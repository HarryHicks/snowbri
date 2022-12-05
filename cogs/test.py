
from discord.ext import commands

class Test(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.hybrid_command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def hi(self, ctx):
        await ctx.reply(f"Hello {ctx.author.mention}")

async def setup(client):
    await client.add_cog(Test(client))