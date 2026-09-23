import os
import telebot
from yt_dlp import YoutubeDL

# Seu token configurado automaticamente:
API_TOKEN = '8998130586:AAE-Q11yHRBBoDT3JCoCz2_kr3kBDj32gyk'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "👋 Olá! Me envie o link de um vídeo que eu vou baixá-lo para você!")

@bot.message_handler(func=lambda message: True)
def download_and_send_video(message):
    url = message.text
    
    if not url.startswith("http"):
        bot.reply_to(message, "❌ Por favor, envie um link válido.")
        return

    msg_status = bot.reply_to(message, "⏳ Processando e baixando o vídeo... Aguarde.")

    ydl_opts = {
        'format': 'balthas/mp4/best',
        'outtmpl': 'video_downloaded.mp4',
        'quiet': True
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        bot.edit_message_text("📤 Enviando o vídeo para o Telegram...", msg_status.chat.id, msg_status.message_id)
        
        with open('video_downloaded.mp4', 'rb') as video:
            bot.send_video(message.chat.id, video)
            
        os.remove('video_downloaded.mp4')
        bot.delete_message(msg_status.chat.id, msg_status.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ Erro ao baixar o vídeo. Verifique o link.", msg_status.chat.id, msg_status.message_id)
        if os.path.exists('video_downloaded.mp4'):
            os.remove('video_downloaded.mp4')

print("🤖 Bot configurado.")
bot.infinity_polling()
