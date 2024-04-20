import nextcord, os, json, datetime, random
from nextcord.ext import commands
from datetime import datetime
from colorama import Fore

cooldowns = {}

if os.path.exists("./stats/cooldowns.json"):
    try:
        with open("./stats/cooldowns.json", "r") as file:
            cooldowns = json.load(file)
    except json.JSONDecodeError:
        print(Fore.RED + "<-> Failed to load cooldowns.")
        cooldowns = {}

class fgen(commands.Cog):
    intents = nextcord.Intents.all()
    bot = commands.Bot(intents=intents, help_command=None)

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.GREEN + f"<+> /{self.__class__.__name__} command is ready to use!")

    def load_cooldowns(self):
        if os.path.exists("cooldowns.json"):
            try:
                with open("cooldowns.json", "r") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print(Fore.RED + "<-> Failed to load cooldowns.")
        return {}
    
    def save_cooldowns(self):
        with open("cooldowns.json", "w") as file:
            json.dump(cooldowns, file)

    async def check_cooldown(self, ctx, user_level):
        user_id = str(ctx.user.id)
        if user_level in cooldowns and user_id in cooldowns[user_level]["timestamp"]:
            last_time = cooldowns[user_level]["timestamp"][user_id]
            cooldown_time = cooldowns[user_level]["time"]
            current_time = datetime.timestamp(datetime.now())
            if current_time - last_time < cooldown_time:
                remaining_time = round(cooldown_time - (current_time - last_time))
                return remaining_time
        return None
    
    @bot.slash_command(name="fgen", description="⭐ Generate accounts from the free generating service.")
    async def fgen(self, ctx, stock):
        user_id = str(ctx.user.id)
        user = ctx.user
        user_level = "free"

        if int(ctx.channel.id) != int(os.environ["freeId"]):
            embed = nextcord.Embed(title="❌ An error occured!", description=f"You cannot use our service here, please go to the <#{os.environ['freeId']}> channel.", color=nextcord.Colour.red())
            await ctx.send(embed=embed, ephemeral=True)
            print(Fore.RED + f"<-> Failed to generate a {stock} account, user {user} did not use the right channel.")
            return

        stock = stock.lower() + ".txt"
        if stock not in os.listdir("fstock//"):
            embed = nextcord.Embed(title="❌ An error occured!", description="The service that you tried to generate doesn't exist.", color=nextcord.Colour.red())
            await ctx.send(embed=embed, ephemeral=True)
            print(Fore.RED + f"<-> Failed to generate, service doesn't exist.")
            return
        
        cooldown_remaining = await self.check_cooldown(ctx, user_level)
        if cooldown_remaining:
            embed = nextcord.Embed(title="❌ An error occured!", description=f"You are on cooldown, please wait `{cooldown_remaining}` seconds to generate again.", color=nextcord.Colour.red())
            await ctx.send(embed=embed, ephemeral=True)
            print(Fore.RED + f"<-> Failed to generate a {stock} account, user {user} is on cooldown.")
            return
        
        if user_level not in cooldowns:
            cooldowns[user_level] = {"time": 60, "timestamp": {}}
        cooldowns[user_level]["timestamp"][user_id] = datetime.timestamp(datetime.now())
        self.save_cooldowns()
        
        embed = nextcord.Embed(title="⏰ Please wait..", description="> I am getting the account ready for you, please wait a few seconds..\n\nIf this takes more than 15 seconds, please contact the staff team to check bot's console.", color=nextcord.Colour.yellow())
        embed.set_footer(text="Use the bot in your server: https://github.com/zkoolmao/Account-Generator-Bot", icon_url="https://cdn.discordapp.com/attachments/1204244617869000788/1204249308237402162/icon.png?ex=65d40b90&is=65c19690&hm=42115bccb811f86d7a9cdbcb686a2f1c2a5be6633e04f712da3765d6da475e03&")
        msg = await ctx.send(embed=embed)
        print(Fore.GREEN + f"<+> Getting a {stock} account ready for user {user}...")

        with open(f"fstock/{stock}") as file:
            lines = file.read().splitlines()
            if len(lines) == 0:
                embed = nextcord.Embed(title="❌ An error occured!", description="> The service that you tried to generate is currently out of stock, try again later.")
                await msg.edit(embed=embed)
                print(Fore.RED + f"<-> Failed to get a {stock} account for {user}, service out of stock.")
                return
            else:
                name = (stock[0].upper() + stock[1:].lower()).replace(".txt", "")
                account = random.choice(lines)
                combo = account.split(":")
                username = combo[0]
                password = combo[1]

                embed = nextcord.Embed(title=f"🎉 {name} Account:", description="> If the account does not, try another one.", color=nextcord.Colour.green())
                embed.add_field(name="Username:", value=f"```{username}```", inline=True)
                embed.add_field(name="Password:", value=f"```{password}```", inline=True)
                embed.add_field(name="Combo:", value=f"```{account}```", inline=False)
                embed.set_footer(text="Use the bot in your server: https://github.com/zkoolmao/Account-Generator-Bot", icon_url="https://cdn.discordapp.com/attachments/1204244617869000788/1204249308237402162/icon.png?ex=65d40b90&is=65c19690&hm=42115bccb811f86d7a9cdbcb686a2f1c2a5be6633e04f712da3765d6da475e03&")
                embed.timestamp = datetime.now()
                
                try:
                    dm = await ctx.user.send(f"{account}", embed=embed)
                    print(Fore.GREEN + f"<+> Successfully sent a {stock} account to {user}.")
                except:
                    print(Fore.RED + f"<-> {user}'s DMs are closed, couldn't send a {stock} account.")

                lines.remove(account)
                with open(f"fstock//{stock}", "w", encoding='utf-8') as file:
                    file.write("\n".join(lines))

            try:
                dmlink = dm.jump_url

                embed = nextcord.Embed(title=f"🎉 Successfully generated a {name} account!", description=f"> Check your [DMs]({dmlink}) or the message below for your account.\n\n**Report any issues to the staff team!**", color=nextcord.Colour.green())
                embed.timestamp = datetime.now()
                embed.set_footer(text="Use the bot in your server: https://github.com/zkoolmao/Account-Generator-Bot", icon_url="https://cdn.discordapp.com/attachments/1204244617869000788/1204249308237402162/icon.png?ex=65d40b90&is=65c19690&hm=42115bccb811f86d7a9cdbcb686a2f1c2a5be6633e04f712da3765d6da475e03&")
                await msg.edit(embed=embed)
            except:
                embed = nextcord.Embed(title=f"🎉 Successfully generated a {name} account!", description=f"> Check the message below for your account.\n\n**Report any issues to the staff team!**", color=nextcord.Colour.green())
                embed.timestamp = datetime.now()
                embed.set_footer(text="Use the bot in your server: https://github.com/zkoolmao/Account-Generator-Bot", icon_url="https://cdn.discordapp.com/attachments/1204244617869000788/1204249308237402162/icon.png?ex=65d40b90&is=65c19690&hm=42115bccb811f86d7a9cdbcb686a2f1c2a5be6633e04f712da3765d6da475e03&")
                await msg.edit(embed=embed)

            embed = nextcord.Embed(title=f"🎉 {name} Account:", description="> If the account does not work, try another one.", color=nextcord.Colour.green())
            embed.add_field(name="Username:", value=f"```{username}```", inline=True)
            embed.add_field(name="Password:", value=f"```{password}```", inline=True)
            embed.add_field(name="Combo:", value=f"```{account}```", inline=False)
            embed.timestamp = datetime.now()
            embed.set_footer(text="Use the bot in your server: https://github.com/zkoolmao/Account-Generator-Bot", icon_url="https://cdn.discordapp.com/attachments/1204244617869000788/1204249308237402162/icon.png?ex=65d40b90&is=65c19690&hm=42115bccb811f86d7a9cdbcb686a2f1c2a5be6633e04f712da3765d6da475e03&")
            await ctx.send(f"{username}:{password}", embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(fgen(bot))
