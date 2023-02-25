from pyrogram import Client
from .Config import Config
bot = Client("s",api_id=Config.API_ID,
api_hash=Config.API_HASH,
bot_token=Config.BOT_TOKEN,
plugins=dict(root=f"{__main__}/plugins")
)

with bot:
    BotId=bot.me.id
    BotUN=bot.me.username