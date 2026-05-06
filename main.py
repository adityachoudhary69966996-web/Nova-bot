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
    return "✅ NØVĀ's VERY LONG ALL-ROUNDER BOT is Running 24/7 🔥"

# ==================== BOT SETUP ====================
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"✅ NØVĀ's SUPER LONG BOT IS FULLY ONLINE → {bot.user}")
    print(f"Connected to {len(bot.guilds)} servers | Ready for everything!")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)

# ==================== STORAGE ====================
money = {}
levels = {}
xp = {}
warnings = {}

# ==================== MULTI / REPEAT SECTION ====================
@bot.command(aliases=["multi", "multimsg"])
async def multi(ctx, times: int, *, text="hi"):
    """!multi 5 hello"""
    if times > 20:
        times = 20
        await ctx.send("⚠️ Max 20 messages!")
    for _ in range(times):
        await ctx.send(text)
        await asyncio.sleep(0.6)

@bot.command(name="say", aliases=["repeat", "echo", "tell", "parrot"])
async def say_command(ctx, *, text=None):
    if not text:
        return await ctx.send("Usage: `!say Your message`")
    await ctx.send(text)

@bot.command()
async def spam(ctx, times: int = 5, *, text="NØVĀ Bot 🔥"):
    if times > 15: times = 15
    for _ in range(times):
        await ctx.send(text)
        await asyncio.sleep(0.7)

# ==================== DM SYSTEM ====================
@bot.command()
async def dm(ctx, user: discord.User, *, message=None):
    if not message:
        return await ctx.send("Usage: `!dm @user Your message`")
    try:
        await user.send(f"**📱 Message from {ctx.author}**\n\n{message}\n\n─ Sent via NØVĀ's Bot")
        await ctx.send(f"✅ DM sent to **{user}**")
    except:
        await ctx.send("❌ Could not send DM")

@bot.command()
async def dmall(ctx, *, message):
    sent = 0
    for member in ctx.guild.members:
        if member.bot: continue
        try:
            await member.send(f"**Broadcast from {ctx.author}**\n\n{message}")
            sent += 1
            await asyncio.sleep(1)
        except:
            pass
    await ctx.send(f"✅ Sent to {sent} members")

# ==================== ADMIN / MOD COMMANDS ====================
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
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member_name):
    banned = await ctx.guild.bans()
    for entry in banned:
        if str(entry.user) == member_name or entry.user.name == member_name:
            await ctx.guild.unban(entry.user)
            await ctx.send(f"✅ Unbanned {entry.user}")
            return
    await ctx.send("User not found")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not role:
        role = await ctx.guild.create_role(name="Muted", permissions=discord.Permissions(send_messages=False))
    await member.add_roles(role)
    await ctx.send(f"🔇 Muted {member}")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if role:
        await member.remove_roles(role)
        await ctx.send(f"🔊 Unmuted {member}")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int = 20):
    if amount > 100: amount = 100
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 Purged {amount} messages", delete_after=3)

# ==================== LEVEL SYSTEM ====================
@bot.event
async def on_message(message):
    if message.author.bot: return
    user = message.author.id
    xp[user] = xp.get(user, 0) + random.randint(5, 20)
    current_level = levels.get(user, 1)
    if xp[user] >= current_level * 120:
        levels[user] = current_level + 1
        xp[user] = 0
        await message.channel.send(f"🎉 {message.author.mention} leveled up to **Level {levels[user]}**!")
    await bot.process_commands(message)

@bot.command()
async def level(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(f"📊 **{member}** → Level **{levels.get(member.id, 1)}** | XP **{xp.get(member.id, 0)}**")

@bot.command()
async def leaderboard(ctx):
    sorted_list = sorted(levels.items(), key=lambda x: x[1], reverse=True)[:15]
    msg = "**🏆 Top 15 Leaderboard**\n"
    for i, (uid, lvl) in enumerate(sorted_list, 1):
        try:
            user = await bot.fetch_user(uid)
            msg += f"{i}. {user} — Level {lvl}\n"
        except:
            pass
    await ctx.send(msg)

# ==================== ECONOMY ====================
@bot.command()
async def earn(ctx):
    amount = random.randint(30, 100)
    money[ctx.author.id] = money.get(ctx.author.id, 0) + amount
    await ctx.send(f"💰 You earned **{amount}** coins! Balance: **{money[ctx.author.id]}**")

@bot.command(aliases=["bal", "balance", "coins"])
async def money(ctx):
    await ctx.send(f"💵 **{ctx.author.mention}** has **{money.get(ctx.author.id, 0)}** coins")

@bot.command()
async def give(ctx, member: discord.Member, amount: int):
    if amount <= 0: return await ctx.send("Positive amount only!")
    if money.get(ctx.author.id, 0) < amount:
        return await ctx.send("❌ Not enough coins!")
    money[ctx.author.id] -= amount
    money[member.id] = money.get(member.id, 0) + amount
    await ctx.send(f"✅ Gave **{amount}** coins to {member.mention}")

# ==================== FUN COMMANDS ====================
@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! `{round(bot.latency*1000)}ms`")

@bot.command(aliases=["hi", "hey", "sup"])
async def hello(ctx):
    await ctx.send(f"Yo {ctx.author.mention}! NØVĀ's Long Bot here 🔥")

@bot.command()
async def joke(ctx):
    jokes = [
        "Why do programmers prefer dark mode? Light attracts bugs! 😂",
        "Why was the JavaScript developer sad? He didn't know how to 'null' his feelings.",
        "I'm reading a book on anti-gravity. It's impossible to put down!",
        "Why do Python programmers have lamps? Because they prefer light mode? No wait..."
    ]
    await ctx.send(random.choice(jokes))

@bot.command(name="8ball")
async def eight_ball(ctx, *, question=None):
    if not question: return await ctx.send("Ask a question!")
    answers = ["Yes!", "No!", "Maybe...", "Definitely yes", "Very doubtful", "Ask again later"]
    await ctx.send(f"🎱 **Answer:** {random.choice(answers)}")

@bot.command()
async def slap(ctx, member: discord.Member):
    await ctx.send(f"{ctx.author.mention} slapped {member.mention} 👋")

@bot.command()
async def hug(ctx, member: discord.Member):
    await ctx.send(f"{ctx.author.mention} hugged {member.mention} 🤗")

@bot.command()
async def kiss(ctx, member: discord.Member):
    await ctx.send(f"{ctx.author.mention} kissed {member.mention} 😘")

# ==================== HELP ====================
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="⚡ NØVĀ's VERY LONG BOT", color=0x00ffff, timestamp=datetime.datetime.now())
    embed.add_field(name="🔁 Multi & Repeat", value="`!multi <number> <text>`\n`!say` `!spam`", inline=False)
    embed.add_field(name="📱 DM", value="`!dm @user message`\n`!dmall`", inline=False)
    embed.add_field(name="🛠️ Admin", value="`!kick` `!ban` `!mute` `!unmute` `!purge`", inline=False)
    embed.add_field(name="📊 Levels", value="`!level` `!leaderboard`", inline=False)
    embed.add_field(name="💰 Economy", value="`!earn` `!bal` `!give`", inline=False)
    embed.add_field(name="😂 Fun", value="`!ping` `!hello` `!joke` `!8ball` `!slap` `!hug` `!kiss`", inline=False)
    embed.set_footer(text="Made for NØVĀ • Very Long Version")
    await ctx.send(embed=embed)

def run_bot():
    bot.run(os.getenv("TOKEN"))

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=os.getenv("PORT", 8080))