import nextcord, os
from nextcord.ext import commands
from colorama import Fore

intents = nextcord.Intents.all()
bot = commands.Bot(intents=intents, help_command=None)

@bot.event
async def on_ready():
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.playing,name="/help to get started!"), status=nextcord.Status.idle)
    print(Fore.GREEN + f"<+> Running as {bot.user}")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run("")
