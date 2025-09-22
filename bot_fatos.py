import discord
import requests
import os
from discord.ext import tasks, commands
from datetime import datetime

# Pega o token e ID do canal das variáveis de ambiente do Railway
TOKEN = os.getenv("97cf3df1c129851c56b85f3867d701c4c331b0c4d7eb3ccf3dab5e465c43b9ed")
CHANNEL_ID = int(os.getenv("1419380401599811584"))

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

def get_fact():
    try:
        # Exemplo: pegar fato da Numbers API
        hoje = datetime.now()
        url = f"http://numbersapi.com/{hoje.month}/{hoje.day}/date?json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("text", "Não encontrei um fato hoje.")
        else:
            return "Não consegui buscar o fato do dia."
    except Exception as e:
        return f"Erro ao buscar fato: {e}"

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    send_fact.start()

@tasks.loop(hours=24)
async def send_fact():
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        fact = get_fact()
        await channel.send(f"📅 Fato do dia: {fact}")

bot.run(TOKEN)