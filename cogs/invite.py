import discord
from discord.ext import commands

class invite(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.hybrid_command(name="invite", with_app_command = True, description = "Send the invite to Snowbri!")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def invite(self, ctx):
        embed=discord.Embed(title="Bot Invite", url="https://discord.com/api/oauth2/authorize?client_id=1049392746567303280&permissions=3221538880&scope=bot%20applications.commands", description="Click the link about to add Snowbi to your server!", color=0x06a9c6)
        embed.set_footer(text="Snowbri - Snowy Development")
        await ctx.reply(embed=embed, ephemeral=True)

async def setup(client):
    await client.add_cog(invite(client))
