from . import bot

from asyncio import get_event_loop
from pyrogram import idle

async def main():
    await bot.start()
    await bot.send_message(-1001846218052,"The Bot Started!")
    await idle()

if __name__=="__main__":
    loop=get_event_loop()
    loop.run_until_complete(main())
