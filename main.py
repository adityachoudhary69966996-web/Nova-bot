from flask import Flask
import os
import threading
import discord
from discord.ext import commands
import asyncio
import random
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ NØVĀ's Improved Long Bot is Running 24/7 🔥"

# ==================== BOT SETUP ====================
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"✅ NØVĀ's IMPROVED BOT ONLINE → {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)

# ==================== STORAGE ====================
money = {}
levels = {}
xp = {}

# ==================== MULTI & REPEAT ====================
@bot.command(aliases=["multi", "multimsg"])
async def multi(ctx, times: int, *, text="hi"):
    if times > 25: times = 25
    for _ in range(times):
        await ctx.send(text)
        await asyncio.sleep(0.6)

@bot.command(name="say", aliases=["repeat", "echo"])
async def say_command(ctx, *, text=None):
    if not text: return await ctx.send("Usage: `!say message`")
    await ctx.send(text)

@bot.command()
async def spam(ctx, times: int = 5, *, text="NØVĀ Bot 🔥"):
    if times > 20: times = 20
    for _ in range(times):
        await ctx.send(text)
        await asyncio.sleep(0.7)

# ==================== DM ====================
@bot.command()
async def dm(ctx, user: discord.User, *, message=None):
    if not message: return await ctx.send("Usage: `!dm @user message`")
    try:
        await user.send(f"**Message from {ctx.author}**\n\n{message}")
        await ctx.send(f"✅ DM sent to {user}")
    except:
        await ctx.send("❌ DM failed")

# ==================== ADMIN ====================
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason"):
    await member.kick(reason=reason)
    await ctx.send(f"👢 Kicked {member}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 Banned {member}")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int = 20):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"Purged {amount} messages", delete_after=3)

# ==================== ECONOMY + GAMBLING (OwO Style) ====================
@bot.command()
async def earn(ctx):
    amount = random.randint(30, 100)
    money[ctx.author.id] = money.get(ctx.author.id, 0) + amount
    await ctx.send(f"💰 +{amount} coins! Balance: **{money[ctx.author.id]}**")

@bot.command(aliases=["bal", "balance"])
async def money(ctx):
    await ctx.send(f"💵 {ctx.author.mention} has **{money.get(ctx.author.id, 0)}** coins")

@bot.command()
async def gamble(ctx, amount: int):
    if amount <= 0: return await ctx.send("Bet positive amount!")
    if money.get(ctx.author.id, 0) < amount:
        return await ctx.send("❌ Not enough coins!")
    
    if random.random() < 0.5:  # 50% win chance
        win = amount * 2
        money[ctx.author.id] += win
        await ctx.send(f"🎰 **YOU WON!** +{win} coins! New Balance: **{money[ctx.author.id]}**")
    else:
        money[ctx.author.id] -= amount
        await ctx.send(f"💸 You lost **{amount}** coins... Balance: **{money[ctx.author.id]}**")

@bot.command()
async def bet(ctx, amount: int):
    await gamble(ctx, amount)  # alias

# ==================== FUN & INTERACTION ====================
@bot.command()
async def hug(ctx, member: discord.Member):
    await ctx.send(f"{ctx.author.mention} hugged {member.mention} 🤗❤️")

@bot.command()
async def kiss(ctx, member: discord.Member):
    await ctx.send(f"{ctx.author.mention} kissed {member.mention} 😘")

@bot.command()
async def slap(ctx, member: discord.Member):
    await ctx.send(f"{ctx.author.mention} slapped {member.mention} 👋💥")

# ==================== CHATBOT ====================
@bot.command()
async def chatbot(ctx, *, message=None):
    if not message:
        return await ctx.send("Usage: `!chatbot How are you?`")
    
    responses = [
        "I'm doing great, thanks for asking! 🔥",
        "Bro same pinch, how about you?",
        "That's interesting... tell me more!",
        "Haha true dat!",
        "I'm just a bot but I'm vibing with you 😎",
        "No cap, that's facts!",
        "Lmao you're funny bro",
        "I'm NØVĀ's bot, always ready to chat!"
    ]
    await ctx.send(random.choice(responses))

# ==================== 8BALL (Fixed) ====================
@bot.command(name="8ball")
async def eight_ball(ctx, *, question=None):
    if not question:
        return await ctx.send("Usage: `!8ball Will I win today?`")
    answers = ["Yes!", "No!", "Maybe...", "Definitely yes", "Very doubtful", "Outlook good", "Don't count on it", "100% yes", "Ask again later"]
    await ctx.send(f"🎱 **Question:** {question}\n**Answer:** {random.choice(answers)}")

# ==================== JOKES (Bigger List) ====================
@bot.command()
async def joke(ctx):
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs! 😂",
        "Why was the JavaScript developer sad? He didn't know how to 'null' his feelings.",
        "I'm reading a book on anti-gravity. It's impossible to put down!",
        "Why do Python developers never get lost? They always follow the `path`!",
        "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
        "Why did the scarecrow win an award? He was outstanding in his field!",
        "Why don't skeletons fight each other? They don't have the guts.",
        "Why was the math book sad? It had too many problems."
    ]
    await ctx.send(random.choice(jokes))

# ==================== MUSIC ====================
@bot.command()
async def play(ctx, *, search=None):
    if not search:
        return await ctx.send("Usage: `!play song name`")
    await ctx.send(f"🎵 Searching for **{search}**...\n\nFull advanced music (YouTube queue, pause, skip) needs extra setup.\nFor now using basic mode.")

@bot.command()
async def stop(ctx):
    await ctx.send("⏹️ Music stopped (placeholder)")

# ==================== HELP ====================
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="⚡ NØVĀ's Improved Long Bot", color=0x00ffff)
    embed.add_field(name="🔁 Repeat", value="`!multi <num> <text>`\n`!say`", inline=False)
    embed.add_field(name="💰 Economy + Gamble", value="`!earn` `!bal` `!gamble <amount>` `!bet <amount>`", inline=False)
    embed.add_field(name="📱 DM", value="`!dm @user message`", inline=False)
    embed.add_field(name="🛠️ Admin", value="`!kick` `!ban` `!purge`", inline=False)
    embed.add_field(name="😂 Fun", value="`!chatbot <message>`\n`!8ball <question>`\n`!joke`\n`!hug` `!kiss` `!slap`", inline=False)
    embed.add_field(name="🎵 Music", value="`!play <song>`", inline=False)
    await ctx.send(embed=embed)

def run_bot():
    bot.run(os.getenv("TOKEN"))

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=os.getenv("PORT", 8080))