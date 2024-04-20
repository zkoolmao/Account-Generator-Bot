import nextcord, datetime
from nextcord.ext import commands
from datetime import datetime
from colorama import Fore

class help(commands.Cog):
    intents = nextcord.Intents.all()
    bot = commands.Bot(intents=intents, help_command=None)

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.GREEN + f"<+> /{self.__class__.__name__} command is ready to use!")
    
    @bot.slash_command(name="help", description="📚 Display the list of all of our commands.")
    async def help(self, ctx):
        embed = nextcord.Embed(title="📚 Command List:", timestamp=datetime.utcnow(), color=nextcord.Colour.green())
        embed.set_footer(text="Free Version: https://github.com/zkoolmao/Account-Generator-Bot", icon_url="https://cdn.discordapp.com/attachments/1204244617869000788/1204249308237402162/icon.png?ex=65d40b90&is=65c19690&hm=42115bccb811f86d7a9cdbcb686a2f1c2a5be6633e04f712da3765d6da475e03&")
        embed.add_field(name="/fgen", value="Generates accounts from the free generating service.", inline=False)
        embed.add_field(name="/fstock", value="Displays the list of our account stock.", inline=False)
        embed.add_field(name="/help", value="Displays this command.", inline=False)
    
        await ctx.send(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(help(bot))
