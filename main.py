import os
import telebot
from yt_dlp import YoutubeDL


API_TOKEN = '8880654461:AAHGQbEEQ8sEzos_R4HZDD5mT1HfSWh5PnE'
bot = telebot.TeleBot(token=API_TOKEN)



@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Olá! Envie um link do TikTok, Shopee, Mercado Livre, Instagram ou Facebook e eu irei baixar o vídeo para você! 🎬")

@bot.message_handler(func=lambda message: True)
def download_and_send_video(message):
    url = message.text
    
    # Filtro simples para aceitar links comuns enviados pelo celular
    if "http://" in url or "https://" in url:
        msg_espera = bot.reply_to(message, "✅ Seu link foi adicionado à fila de download! Por favor, aguarde alguns instantes... ⏳")
        
        # Configuração para extrair o melhor formato mp4 disponível
        ydl_opts = {
            'outtmpl': 'video_baixado.mp4',
            'format': 'best[ext=mp4]/best',
            'quiet': True,
            'no_warnings': True
        }
        
        try:
            # Baixa o vídeo direto no servidor da Render
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # Envia o vídeo de volta para o usuário no Telegram
            with open('video_baixado.mp4', 'rb') as video:
                bot.send_video(message.chat.id, video, caption="Aqui está o seu vídeo! 😉")
            
            # Limpa as mensagens e arquivos temporários do servidor
            bot.delete_message(message.chat.id, msg_espera.message_id)
            os.remove('video_baixado.mp4')
            
        except Exception as e:
            bot.edit_message_text("❌ Não consegui extrair o vídeo desse link. Verifique se o produto/post possui um vídeo válido ou tente novamente.", message.chat.id, msg_espera.message_id)
            if os.path.exists('video_baixado.mp4'):
                os.remove('video_baixado.mp4')
    else:
        bot.reply_to(message, "❌ Por favor, envie um link válido (começando com http:// ou https://).")

# Inicia o bot ignorando conflitos antigos
bot.infinity_polling(skip_pending=True)
