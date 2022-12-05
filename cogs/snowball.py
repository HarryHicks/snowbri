import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient
import random

# MongoDB configuration
cluster = MongoClient("161.97.184.243:25019")
db = cluster["snowball"]
collection = db["leaderboard"]

class snowball(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.hybrid_command(name="collect", with_app_command = True, description = "Collect a snowball to lob at a friend!")
    # The user can collect only 1 snowball every 30 seconds
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def collect(self, ctx):
        if ctx.author not in self.client.current_users:
            author = ctx.message.author.id

            self.client.current_users.add(ctx.author)
            self.client.counter[author] = 1

            embed = discord.Embed(
                description="Slapping on your warmest pair of gloves, you gathered some snow and started shaping some snowballs. You now have 1 of them—let 'em fly!",
                color=discord.Color.from_rgb(89, 100, 242),
            )
            embed.set_image(
                url="https://images-ext-1.discordapp.net/external/E9ROIdIhkUg5m5OJrxncIKnjM8Gqe4FPcuzi-Bvh_hk/https/c.tenor.com/NBqwJNBaSXUAAAAC/playing-with-snow-piu-piu.gif?width=400&height=225"
            )
            await ctx.send(embed=embed)
        else:
            author = ctx.message.author.id

            self.client.current_users.add(ctx.author)
            self.client.counter[author] += 1

            embed = discord.Embed(
                description=f"Slapping on your warmest pair of gloves, you gathered some snow and started shaping some snowballs. You now have {self.client.counter[author]} of them—let 'em fly!",
                color=discord.Color.from_rgb(89, 100, 242),
            )
            embed.set_image(
                url="https://images-ext-1.discordapp.net/external/E9ROIdIhkUg5m5OJrxncIKnjM8Gqe4FPcuzi-Bvh_hk/https/c.tenor.com/NBqwJNBaSXUAAAAC/playing-with-snow-piu-piu.gif?width=400&height=225"
            )
            await ctx.send(embed=embed)

   
    @commands.hybrid_command(name="throw", with_app_command = True, description = "Let your snowball you collected fly!")
    async def throw(self, ctx, user: discord.Member = None):
        if ctx.author in self.client.current_users:
            # If the author doesn't have 0 snowballs
            if self.client.counter[ctx.message.author.id] != 0:
                if user:  # User is mentioned
                    if (
                        user.id == ctx.author.id
                    ):  # If the mentioned user is the author itself
                        embed = discord.Embed(
                            description="You can't throw a snowball at yourself! Unless you like, smush it against your face… so choose a fellow server member!",
                            color=discord.Color.from_rgb(254, 1, 0),
                        )
                        await ctx.send(embed=embed)
                    elif (
                        user.id == self.client.user.id
                    ):  # If the mentioned user is the bot itself
                        embed = discord.Embed(
                            description="Why you even try to smush the face of your favourite bot <:catCry:919806075019087933>"
                        )
                        await ctx.send(embed=embed)
                    else:  # The mentioned user is not the author and the bot
                        # The outcome of the snowball throw command
                        outcome = random.choice(self.client.snowball)
                        query1 = {"_id": ctx.author.id}
                        # The user isn't there in the database
                        if collection.count_documents(query1) == 0:
                            if (
                                outcome == "hit"
                            ):  # If the random outcome comes to be hit
                                embed = discord.Embed(
                                    description=f"<@{user.id}> wasn't even paying attention to chat… and they got smacked by a snowball anyways! Hey <@{user.id}> — use `/collect`, then `/throw` to get 'em back!",
                                    color=discord.Color.from_rgb(97, 254, 96),
                                )
                                embed.set_image(
                                    url="https://media.giphy.com/media/W5TBt9C4VVWw2BOOjP/giphy.gif"
                                )
                                await ctx.send(embed=embed)
                                self.client.counter[ctx.message.author.id] -= 1
                                post_author = {
                                    "_id": ctx.author.id,
                                    "hit": 1,
                                    "miss": 0,
                                    "ko": 0,
                                }
                                collection.insert_one(post_author)
                                post_user = {
                                    "_id": user.id,
                                    "hit": 0,
                                    "miss": 0,
                                    "ko": 1,
                                }
                                collection.insert_one(post_user)
                            else:  # If the random outcome comes to be miss
                                embed = discord.Embed(
                                    description="You throw a snowball with all your might, just for it to land a few inches from your feet. You missed! Maybe you should work on your arm strength a bit...",
                                    color=discord.Color.from_rgb(255, 167, 1),
                                )
                                embed.set_image(
                                    url="https://media.giphy.com/media/ukSGgGljsKRXdiHb0h/giphy.gif"
                                )
                                await ctx.send(embed=embed)
                                self.client.counter[ctx.message.author.id] -= 1
                                post_author = {
                                    "_id": ctx.author.id,
                                    "hit": 0,
                                    "miss": 1,
                                    "ko": 0,
                                }
                                collection.insert_one(post_author)

                        else:
                            if (
                                outcome == "hit"
                            ):  # If the random outcome comes to be hit
                                embed = discord.Embed(
                                    description=f"<@{user.id}> wasn't even paying attention to chat… and they got smacked by a snowball anyways! Hey <@{user.id}> — use `/collect`, then `/throw` to get 'em back!",
                                    color=discord.Color.from_rgb(97, 254, 96),
                                )
                                embed.set_image(
                                    url="https://media.giphy.com/media/W5TBt9C4VVWw2BOOjP/giphy.gif"
                                )
                                await ctx.send(embed=embed)
                                self.client.counter[ctx.message.author.id] -= 1
                                query_author = {"_id": ctx.author.id}
                                hit_query = collection.find(query_author)
                                for result_hit in hit_query:
                                    hit_score = result_hit["hit"]
                                    hit_score = hit_score + 1

                                query_user = {"_id": user.id}
                                ko_query = collection.find(query_user)
                                for result_ko in ko_query:
                                    global koscore
                                    koscore = result_ko["ko"]
                                    koscore += 1

                                collection.update_one(
                                    {"_id": ctx.author.id}, {"$set": {"hit": hit_score}}
                                )
                                collection.update_one(
                                    {"_id": user.id}, {"$set": {"ko": koscore}}
                                )
                            else:  # If the random outcome comes to be miss
                                embed = discord.Embed(
                                    description="You throw a snowball with all your might, just for it to land a few inches from your feet. You missed! Maybe you should work on your arm strength a bit...",
                                    color=discord.Color.from_rgb(255, 167, 1),
                                )
                                embed.set_image(
                                    url="https://media.giphy.com/media/ukSGgGljsKRXdiHb0h/giphy.gif"
                                )
                                await ctx.send(embed=embed)
                                self.client.counter[ctx.message.author.id] -= 1
                                query_author = {"_id": ctx.author.id}
                                miss_query = collection.find(query_author)
                                for result1 in miss_query:
                                    miss_score = result1["miss"]
                                    miss_score = miss_score + 1

                                collection.update_one(
                                    {"_id": ctx.author.id},
                                    {"$set": {"miss": miss_score}},
                                )
                else:  # The user isn't mentioned
                    embed = discord.Embed(
                        description="<:cryangry:919806697407664169> Mention a fellow server member to smush their face",
                        color=discord.Color.from_rgb(255, 1, 1),
                    )
                    await ctx.send(embed=embed)
            else:  # The user is out of snowballs
                embed = discord.Embed(
                    description="Oops! You don't have any snowballs. Use the `/collect` command to stock up!",
                    color=discord.Color.from_rgb(254, 167, 0),
                )
                await ctx.send(embed=embed)
        else:
            return



    

    @commands.hybrid_command(name="stats", with_app_command = True, description = "View the statistics of someone. Don't include a member to check yours.")
    async def stats(self, ctx, user: discord.Member = None):
        if user is None:  # If the user is not  been mentioned => The author wants to see his stats
            stats = collection.find_one({"_id": ctx.author.id})
            embed = discord.Embed(
                title=f"Stats of {ctx.author.name}", color=discord.Color.from_rgb(88, 101, 242))
            embed.add_field(name="Hits", value=stats["hit"], inline=True)
            embed.add_field(name="Misses", value=stats["miss"], inline=True)
            embed.add_field(name="KO's", value=stats["ko"], inline=True)
            await ctx.send(embed=embed)
        else:  # If the user is been mentioned => The wants to check the stats of other user
            try:  # The user is there in the database
                stats = collection.find_one({"_id": user.id})
                embed = discord.Embed(
                    title=f"Stats of {user.name}", color=discord.Color.from_rgb(88, 101, 242))
                embed.add_field(name="Hits", value=stats["hit"], inline=True)
                embed.add_field(name="Misses", value=stats["miss"], inline=True)
                embed.add_field(name="KO's", value=stats["ko"], inline=True)
                await ctx.send(embed=embed)
            except TypeError:  # The user isn't there in the database
                await ctx.send("That player doesn't have any stats <:catAngry:919806075606286386>")
async def setup(client):
    await client.add_cog(snowball(client))
