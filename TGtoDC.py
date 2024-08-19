import requests
import tempfile
import os
from telegram.ext import Updater, MessageHandler, Filters
import telegram

os.system('clear')


TOKEN = "Bot Token"
CHANNEL_ID = "Channel ID"

DISCORD_WEBHOOK_URL = "Discord WebHook"

def header():
    print("""


░▒▓████████▓▒░▒▓██████▓▒░       ░▒▓████████▓▒░▒▓██████▓▒░       ░▒▓███████▓▒░ ░▒▓██████▓▒░  
   ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░         ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
   ░▒▓█▓▒░  ░▒▓█▓▒░                ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
   ░▒▓█▓▒░  ░▒▓█▓▒▒▓███▓▒░         ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
   ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░         ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
   ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░         ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
   ░▒▓█▓▒░   ░▒▓██████▓▒░          ░▒▓█▓▒░   ░▒▓██████▓▒░       ░▒▓███████▓▒░ ░▒▓██████▓▒░  
                                                                                            
                                                                                        
                             Coded By: StealthFoX (Shad) - WWW.CYB3R.ARMY
                                         t.me/xByteBlitzX                                                                               

""")
    
header()


def forward_to_discord(update, context):
    channel_post = update.channel_post
    
    print("Received update:", update)
    
    sender_name = channel_post.chat.username if channel_post.chat.username else channel_post.chat.title
    
    if channel_post.text:
        text = channel_post.text
        payload = {
            "content": f"**{sender_name}:** {text}"
        }
        
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        
        if response.status_code != 200:
            print(f"Failed to forward message to Discord: {response.text}")
    
    if channel_post.photo:
        photo = channel_post.photo[-1] 
        file_id = photo.file_id
        file_obj = context.bot.get_file(file_id)
        photo_url = file_obj.file_path
        
        photo_file = requests.get(photo_url)
        
        payload = None
        
        if channel_post.caption:
            caption = channel_post.caption
            payload = {
                "content": f"**{sender_name} sent a photo with caption:** {caption}",
            }
        
        if not payload:
            payload = {
                "content": f"**{sender_name} sent a photo:**",
            }
        
        files = {"photo": ("photo.jpg", photo_file.content, "image/jpeg")}
        response = requests.post(DISCORD_WEBHOOK_URL, data=payload, files=files)
        
        if response.status_code != 200:
            print(f"Failed to forward photo to Discord: {response.text}")


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(MessageHandler(Filters.chat(CHANNEL_ID) & ~Filters.forwarded, forward_to_discord))
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()