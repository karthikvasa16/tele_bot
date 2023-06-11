import telebot
import pytesseract
from PIL import Image
from gtts import gTTS
import playsound
import os

# Telegram bot token
bot_token = '6102789034:AAE7S9whz67Z6HOoq1iLXCE1PkrqSzqlnTw'

# Create a new Telegram bot instance
bot = telebot.TeleBot(bot_token)

# Handler for processing incoming photo messages
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # Get the photo file ID
    file_id = message.photo[-1].file_id

    # Get the photo file object
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path

    # Download the photo using the file path
    image_path = bot.download_file(file_path)

    # Convert the downloaded image to text using pytesseract
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)

    # Save the text as speech
    tts = gTTS(text=text, lang='en')
    speech_file = 'output_speech.mp3'
    tts.save(speech_file)

    # Send the speech file as an audio message
    with open(speech_file, 'rb') as audio:
        bot.send_audio(message.chat.id, audio)

    # Cleanup: Delete the downloaded image and speech file
    os.remove(image_path)
    os.remove(speech_file)

# Start the bot
bot.polling()
