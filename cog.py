__authors__ = 'aejb'
import datetime
import json
import math
import numpy

import discord
import requests
import aiohttp
import asyncio
from discord.ext import commands


class ShellCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.shardCount = 4480
        self.testing = 0
        self.stuck_array = []

    async def fetch(self, session, url, ctx):
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                message = "Error: HTTP error " + str(response.status)
                await ctx.channel.send(message)

    async def getJSON(self, ctx):
        async with aiohttp.ClientSession() as session:
            if self.testing == 0:
                raw = await self.fetch(session, "https://status.rythmbot.co/raw", ctx)
            else:
                raw = await self.fetch(session, "http://cdn.dvorak.host/test.json", ctx)
            raw_json = json.loads(raw)
            return raw_json

    async def getAJAX(self, ctx, guild_id):
        async with aiohttp.ClientSession() as session:
            combined = str("https://web.rythmbot.co/ajax/shard/" + str(guild_id))
            ajax = await self.fetch(session, combined, ctx)
            ajax_json = json.loads(ajax)
            return ajax_json

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed()

        embed.add_field(name="Command",
                        value="ri hello\nri help\nri [guild | g] {gID}\nri [shard | s] {sID}\nri [cluster | c] {cID}\nri [status | i]\nri [clusterinfo | ci]\nri check",
                        inline=True)
        embed.add_field(name="Use",
                        value="A ping command\nShows this command\nShard and Cluster info about a guild \nShard and Cluster info about a shard \nInfo on shard issues about a cluster\nInfo on shard issues by issue type \nInfo on shard issues grouped by cluster \nOutputs the loaded shards ",
                        inline=True)

        await ctx.send(embed=embed)

    @commands.command()
    async def hello(self, ctx):
        await ctx.channel.send("oh hi")

    async def on_command_error(self, ctx, error):
        print("\n")
        if isinstance(error, commands.MissingRequiredArgument):
            errorname=str(ctx.command)
            message = "Error: You need to specify a " + errorname + " ID."
            await ctx.channel.send(message)
            print("\ncommandError\t", error)

    async def info(self, ctx, cluster_choice):
        raw = await self.getJSON(ctx)
        found_count = 0
        online_count = 0
        missing_array = []
        status_dict = {"INITIALIZING": [], "INITIALIZED": [], "LOGGING_IN": [], "CONNECTING_TO_WEBSOCKET": [],
                       "IDENTIFYING_SESSION": [], "AWAITING_LOGIN_CONFIRMATION": [], "LOADING_SUBSYSTEMS": [],
                       "CONNECTED": [], "ATTEMPTING_TO_RECONNECT": [], "WAITING_TO_RECONNECT": [],
                       "RECONNECT_QUEUED": [], "DISCONNECTED": [], "SHUTTING_DOWN": [], "SHUTDOWN": [],
                       "FAILED_TO_LOGIN": []}
        string_dict = {"INITIALIZING": "Initialising", "INITIALIZED": "Initialised", "LOGGING_IN": "Logging in",
                       "CONNECTING_TO_WEBSOCKET": "connecting to websocket", "IDENTIFYING_SESSION": "Identifying",
                       "AWAITING_LOGIN_CONFIRMATION": "Awaiting confirmation",
                       "LOADING_SUBSYSTEMS": "Loading subsystems", "CONNECTED": "Websocket is connected",
                       "ATTEMPTING_TO_RECONNECT": "Attempting to reconnect",
                       "WAITING_TO_RECONNECT": "Waiting to reconnect", "RECONNECT_QUEUED": "In reconnect queue",
                       "DISCONNECTED": "Websocket is disconnected", "SHUTTING_DOWN": "Shutting down",
                       "SHUTDOWN": "Shut down", "FAILED_TO_LOGIN": "Failed to log in"}
        for i in raw:
            if cluster_choice == "all" or math.floor(int(i) / int(math.ceil(self.shardCount / 9))) == cluster_choice:
                if raw[str(i)] == "CONNECTED":
                    online_count += 1
                elif raw[str(i)] in status_dict:
                    status_dict[raw[str(i)]].append(str(i))
                else:
                    missing_array.append(str(i))
        if cluster_choice == "all":
            command_type = ""
        else:
            command_type = "Cluster " + cluster_choice
        if online_count == found_count:
            embed = discord.Embed(colour=discord.Colour(0xd0892f),
                                  description="Rythm {} is 100% Online\nThere are 0 issues".format(
                                      command_type))
            embed.set_author(name="Rythm {} Status".format(command_type))
            embed.set_footer(text="a bot by ash#0001")
            await ctx.send(embed=embed)
        else:
            if cluster_choice == "all":
                problems = self.shardCount - online_count
            else:
                problems = found_count - online_count
            embed = discord.Embed(colour=discord.Colour(0xd0892f),
                                  description="Rythm {} is {}% Online\nThere are {} issues".format(
                                      command_type,
                                      str(round((online_count / self.shardCount), 1) * 100), problems))
            embed.set_author(name="Rythm {} Status".format(command_type))
            embed.set_footer(text="a bot by ash#0001")
            for selection in status_dict:
                if len(status_dict[selection]) != 0:
                    embed.add_field(name=string_dict[selection], value=str((len(status_dict[selection]))), inline=False)
                elif len(missing_array) != 0:
                    embed.add_field(name="Data missing", value=str((len(missing_array))), inline=False)
            await ctx.send(embed=embed)

    @commands.command(aliases=["c"])
    async def cluster(self, ctx, *, cluster_choice):
        if not cluster_choice:
            await ctx.channel.send('You need to specify cluster number')
        await ctx.channel.send('Loading...', delete_after=3)
        await self.info(ctx, cluster_choice)

    @commands.command(aliases=["info", "i"])
    async def status(self, ctx):
        await ctx.channel.send('Loading...', delete_after=3)
        cluster_choice = "all"
        await self.info(ctx, cluster_choice)

    @commands.command(aliases=["g"])
    async def guild(self, ctx, guild_id: int):
        await ctx.channel.send('Loading...', delete_after=3)
        python_obj = await self.getAJAX(ctx, guild_id)
        shard_id = int(python_obj["shard"])
        cluster_id = int(python_obj["cluster"])
        embed = discord.Embed(colour=discord.Colour(0xd0892f), description="Info from Guild")
        embed.add_field(name="Guild", value=str(guild_id), inline=False)
        embed.add_field(name="Shard", value=str(shard_id), inline=False)
        embed.add_field(name="Cluster", value=str(cluster_id), inline=False)
        raw_stat = await self.getJSON(ctx)
        embed.add_field(name="Status", value=raw_stat[str(shard_id)], inline=False)
        embed.set_footer(text="a bot by ash#0001")
        await ctx.send(embed=embed)

    @commands.command(aliases=["s"])
    async def shard(self, ctx, shard_id: int):
        await ctx.channel.send('Loading...', delete_after=3)
        embed = discord.Embed(colour=discord.Colour(0xd0892f), description="Info from Shard")
        embed.add_field(name="Shard", value=str(shard_id), inline=False)
        embed.add_field(name="Cluster", value=str(math.floor(int(shard_id) / int(math.ceil(self.shardCount / 9)))),
                        inline=False)
        raw_stat = await self.getJSON(ctx)
        embed.add_field(name="Status", value=raw_stat[str(shard_id)], inline=False)
        embed.set_footer(text="a bot by ash#0001")
        await ctx.send(embed=embed)

    @commands.command(aliases=["ci"])
    async def clusterinfo(self, ctx):
        await ctx.channel.send('Loading...', delete_after=3)
        onlinecount = 0
        issues_array = []
        raw = await self.getJSON(ctx)
        for shard_status in raw:
            if raw[str(shard_status)] == "CONNECTED":
                onlinecount += 1
            else:
                shard_id = int(shard_status)
                cluster_id = math.floor(int(shard_id) / int(math.ceil(self.shardCount / 9)))
                issues_array.append([int(shard_id), cluster_id])
        clusters = []
        clusters.extend([[] for _ in range(9)])
        for shard_issue in issues_array:
            appender = int(shard_issue[1])
            clusters[appender].append([shard_issue[0]])
        problems = self.shardCount - onlinecount
        embed = discord.Embed(colour=discord.Colour(0xd0892f),
                              description="Rythm is {}% Online\nThere are {} issues".format(
                                  str(round((onlinecount / self.shardCount), 4) * 100), problems))
        embed.set_author(name="Rythm Cluster Status")
        iterative = 0
        for j in clusters:
            if len(j) != 0:
                cluster_name = "Cluster " + str(iterative)
                embed.add_field(name=cluster_name, value=str((len(j))), inline=False)
            iterative += 1
        embed.set_footer(text="a bot by ash#0001")
        if problems != 0:
            time_in_minutes = str(datetime.timedelta(seconds=int(problems * (5/16))))
            embed.add_field(name="Expected Resolution Time", value=time_in_minutes, inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def check(self, ctx):
        await ctx.channel.send('Loading...', delete_after=3)
        raw = await self.getJSON(ctx)
        shards_loaded = 0
        for i in raw:
            shards_loaded += 1
        message = str(shards_loaded) + " shards seen and loaded!"
        await ctx.send(message)

    @commands.command()
    async def clear(self, ctx):
        self.stuck_array = []
        await ctx.channel.send('Stuck shard array cleared!', delete_after=3)

    @commands.command()
    async def stuck(self, ctx):
        await ctx.channel.send('Loading...', delete_after=3)
        onlinecount = 0
        raw = await self.getJSON(ctx)
        status_dict = {"INITIALIZING": [], "INITIALIZED": [], "LOGGING_IN": [], "CONNECTING_TO_WEBSOCKET": [],
                       "IDENTIFYING_SESSION": [], "AWAITING_LOGIN_CONFIRMATION": [], "LOADING_SUBSYSTEMS": [],
                       "CONNECTED": [], "ATTEMPTING_TO_RECONNECT": [], "WAITING_TO_RECONNECT": [],
                       "RECONNECT_QUEUED": [], "DISCONNECTED": [], "SHUTTING_DOWN": [], "SHUTDOWN": [],
                       "FAILED_TO_LOGIN": []}
        missing = []
        stuck_compare = []
        for i in raw:
            if raw[str(i)] == "CONNECTED":
                onlinecount += 1
            elif raw[str(i)] in status_dict:
                stuck_compare.append(str(i))
            else:
                missing.append(str(i))
        compared_list = numpy.intersect1d(stuck_compare, self.stuck_array)
        if len(compared_list) > 0:
            embed = discord.Embed(colour=discord.Colour(0xd0892f), description="Stuck shards")
            embed.set_author(name="Rythm Status")
            embed.set_footer(text="a bot by ash#0001")
            pr = "\n".join(compared_list)
            embed.add_field(name="Shard List", value=pr, inline=False)
            await ctx.send(embed=embed)
        elif len(compared_list) == 0:
            embed = discord.Embed(colour=discord.Colour(0xd0892f), description="There are 0 stuck shards")
            embed.add_field(name="Try running the command again in a few minutes", value="This will identify any stuck shards", inline=False)
            embed.set_author(name="Rythm Status")
            embed.set_footer(text="a bot by ash#0001")
            await ctx.send(embed=embed)
        self.stuck_array = stuck_compare

def setup(bot):
    bot.remove_command("help")
    bot.add_cog(ShellCog(bot))
