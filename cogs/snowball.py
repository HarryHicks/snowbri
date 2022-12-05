import discord
from discord.ext import commands

class snowball(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.hybrid_command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def throw(self, ctx):
        await ctx.reply(f"Hello {ctx.author.mention}")

    @commands.hybrid_command()
    # The user can collect only 1 snowball every 30 seconds
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def collect(self, ctx):
        if ctx.author not in self.client.current_users:
            author = ctx.message.author.id
    
            self.client.current_users.add(ctx.author)
            self.client.counter[author] = 1
    
            embed = discord.Embed(
                description="Slapping on your warmest pair of gloves, you gathered some snow and started shaping some snowballs. You now have 1 of them—let 'em fly!", color=discord.Color.from_rgb(89, 100, 242))
            embed.set_image(
                url="https://images-ext-1.discordapp.net/external/E9ROIdIhkUg5m5OJrxncIKnjM8Gqe4FPcuzi-Bvh_hk/https/c.tenor.com/NBqwJNBaSXUAAAAC/playing-with-snow-piu-piu.gif?width=400&height=225")
            await ctx.send(embed=embed)
        else:
            author = ctx.message.author.id
    
            self.client.current_users.add(ctx.author)
            self.client.counter[author] += 1
    
            embed = discord.Embed(
                description=f"Slapping on your warmest pair of gloves, you gathered some snow and started shaping some snowballs. You now have {self.client.counter[author]} of them—let 'em fly!", color=discord.Color.from_rgb(89, 100, 242))
            embed.set_image(url="https://images-ext-1.discordapp.net/external/E9ROIdIhkUg5m5OJrxncIKnjM8Gqe4FPcuzi-Bvh_hk/https/c.tenor.com/NBqwJNBaSXUAAAAC/playing-with-snow-piu-piu.gif?width=400&height=225")
            await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(snowball(client))