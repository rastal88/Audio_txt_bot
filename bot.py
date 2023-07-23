import os
import telebot
import speech_recognition
from pydub import AudioSegment
import config

bot = telebot.TeleBot(config.token)

def oga2wav(filename):
    #  function that converts the file format
    new_filename = filename.replace('.oga', '.wav')
    audio = AudioSegment.from_file(filename)
    audio.export(new_filename, format='wav')
    return new_filename


def recognize_speech(oga_filename):
    # function that translates voices into text and deletes used files
    wav_filename = oga2wav(oga_filename)
    recognizer = speech_recognition.Recognizer()

    with speech_recognition.WavFile(wav_filename) as source:
        wav_audio = recognizer.record(source)

    text = recognizer.recognize_google(wav_audio, language='ru')

    if os.path.exists(oga_filename):
        os.remove(oga_filename)

    if os.path.exists(wav_filename):
        os.remove(wav_filename)

    return text


def download_file(bot, file_id):
    # function that downloads a file that the user has sent
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    filename = file_id + file_info.file_path
    filename = filename.replace('/', '_')
    with open(filename, 'wb') as f:
        f.write(downloaded_file)
    return filename


@bot.message_handler(commands=['start'])         # handler that sends a response to the "/start" command
def say_hi(message):
    bot.send_message(message.chat.id,
                     'Привет, ' + message.chat.first_name + '! Запиши аудио-сообщение и я переведу его в текст.')


@bot.message_handler(commands=['help'])          # handler that sends a response to the "/help" command
def say_hi(message):
    bot.send_message(message.chat.id, 'May the force be with you!')


@bot.message_handler(content_types=['voice'])    # handler that sends a text in response to a voice message
def transcript(message):
    # Функция, отправляющая текст в ответ на голосовое
    filename = download_file(bot, message.voice.file_id)
    text = recognize_speech(filename)
    bot.send_message(message.chat.id, text)



bot.polling()
