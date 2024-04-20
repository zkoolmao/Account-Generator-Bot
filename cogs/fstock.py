import nextcord, os, datetime
from nextcord.ext import commands
from datetime import datetime
from colorama import Fore


class fstock(commands.Cog):
    intents = nextcord.Intents.all()
    bot = commands.Bot(intents=intents, help_command=None)

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.GREEN + f"<+> /{self.__class__.__name__} command is ready to use!")
    
    @bot.slash_command(name="fstock", description="📜 Display the list of our account stock.")
    async def fstock(self, ctx):
        embed = nextcord.Embed(title="📜 Free Account Stock:", timestamp=datetime.utcnow(), color=nextcord.Colour.green())
        embed.set_footer(text="Free Version: https://github.com/zkoolmao/Account-Generator-Bot", icon_url="https://cdn.discordapp.com/attachments/1204244617869000788/1204249308237402162/icon.png?ex=65d40b90&is=65c19690&hm=42115bccb811f86d7a9cdbcb686a2f1c2a5be6633e04f712da3765d6da475e03&")
        embed.timestamp = datetime.now()
        embed.description = ""
        for filename in os.listdir("fstock/"):
            with open(f"fstock/{filename}") as f: 
                amount = len(f.read().splitlines())
                name = (filename[0:].lower()).replace(".txt","") 
                embed.description += f"* **{name}**: `{amount}`\n"
    
        await ctx.send(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(fstock(bot))
