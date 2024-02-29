import os

import aiohttp
import discord
from discord.ext import commands
from dotenv import load_dotenv


def discord_bot_send_message(message):
    load_dotenv()
    token = os.environ.get("DISCORD_TOKEN")
    channel_id = 1194560564932919329
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"{bot.user} in now running!")
        # channel = client.get_channel(channel_id)
        # await channel.send(message)
        # await client.close()
        channel = bot.get_channel(channel_id)
        await channel.send(message)
        await bot.close()
        await aiohttp.ClientSession().close()

    # client.run(token)
    bot.run(token)
