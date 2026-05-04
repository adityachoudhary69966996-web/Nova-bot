from flask import Flask
import os
import threading
import discord
from discord.ext import commands

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ NØVĀ's Bot is Running 24/7!"

# ==================== BOT ====================
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"✅ NØVĀ's Bot ONLINE → {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)

@bot.command(name="say", aliases=["repeat", "echo"])
async def say_command(ctx, *, text=None):
    if not text:
        return await ctx.send("Usage: `!say message`")
    await ctx.send(text)

@bot.command()
async def dm(ctx, user: discord.User, *, message=None):
    if not message:
        return await ctx.send("Usage: `!dm @user message`")
    try:
        await user.send(f"**From NØVĀ's Bot**\n\n{message}")
        await ctx.send(f"✅ DM sent to {user}")
    except:
        await ctx.send("❌ DM failed")

@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! `{round(bot.latency*1000)}ms`")

def run_bot():
    bot.run(os.getenv("TOKEN"))

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=os.getenv("PORT", 10000))
