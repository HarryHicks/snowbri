import os
from discord.ext import commands
import discord

intents = discord.Intents.default()  
intents.message_content = True

class Client(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix = commands.when_mentioned_or("snowbri "),
            intents = intents,
            help_command = commands.DefaultHelpCommand(dm_help=True)
        )
    
    async def setup_hook(self): 
        print(f"\033[96mLogged in as {bot.user}\033[00m")
        
        cogs_folder = f"{os.path.abspath(os.path.dirname(__file__))}/cogs"
        for filename in os.listdir(cogs_folder):
            if filename.endswith(".py"):
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"\033[97m    - Loaded {filename[:-3]}\033[00m")
                
        print("Loaded cogs")

bot = Client()
bot.remove_command('help')

@bot.event 
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier
    
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.playing, name="with snowballs! ❄️"))
    
    # Remove comment when need to sync new commands, otherwise ratelimited!
    # await bot.tree.sync()

bot.snowball = ["hit", "hit", "hit", "hit", "hit", "miss", "miss", "miss", "miss", "miss", "miss"] # 5/11 chance of hit
bot.current_users = set()
bot.counter = {}  

@bot.event
async def on_guild_join(guild):
    # get all server integrations
    integrations = await guild.integrations()

    for integration in integrations:
        if isinstance(integration, discord.BotIntegration):
            if integration.application.user.name == bot.user.name:
                bot_inviter = integration.user# returns a discord.User object
                
                # send message to the inviter to say thank you
                await bot_inviter.send("""Thank you for inviting Snowbri!
                
                Please make sure to give your members the Use Application Commands so they are able to interact with the bot, or let them use the **snowbri** prefix.
                
                The main commands are:
                • /collect
                • /throw **mention member**
• /stats
• /invite

Thanks again, and with Hicksy#2047s regards, I hope you enjoy Snowbri!""")
                break


token = "" # don't you dare...

bot.run(token)
