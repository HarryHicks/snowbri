import os
from discord.ext import commands
import discord

intents = discord.Intents.default()  
intents.message_content = True

class Client(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix = commands.when_mentioned_or("!"),
            intents = intents,
            help_command = commands.DefaultHelpCommand(dm_help=True)
        )
    
    async def setup_hook(self): #overwriting a handler
        print(f"\033[31mLogged in as {bot.user}\033[39m")
        cogs_folder = f"{os.path.abspath(os.path.dirname(__file__))}/cogs"
        for filename in os.listdir(cogs_folder):
            if filename.endswith(".py"):
                await bot.load_extension(f"cogs.{filename[:-3]}")
        print("Loaded cogs")

bot = Client()



@bot.event 
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier
    # await bot.tree.sync()
  
bot.remove_command('help')
bot.current_users = set()
bot.counter = {}  # This is the dict which stores the number of snowball the user have
# This is the list which returns random output, which decides whether it's a hit or not
bot.snowball = ["hit", "hit", "miss"]



token = os.environ.get("DISCORD_BOT_SECRET") 
bot.run(token)  # Starts the bot