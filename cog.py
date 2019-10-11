__authors__ = 'aejb'
import json
import math
import numpy
import typing

import discord
import requests
import aiohttp
import asyncio
from discord.ext import commands, tasks
from datetime import datetime, timedelta


class ShellCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.shardCount = 4480
        self.testing = 0
        self.stuck_array = []
        self.live_channel_obj = None
        self.live.start()
        self.index = 0

    def cog_unload(self):
        self.live.cancel()

    @tasks.loop(seconds=3.0)
    async def live(self):
        if self.live_channel_obj is None: return
        else:
            refresh_time = datetime.fromtimestamp(datetime.timestamp(datetime.now()))
            print("refresh", refresh_time)
            embed = discord.Embed(colour=discord.Colour(0x2a60f3),
                                  description="\N{INFORMATION SOURCE} **Live Rythm Status**")
            embed.set_author(name="Rythm Info")
            embed.set_footer(text=refresh_time)
            embed.add_field(name="Rythm is currently {}% online", value="{} shards connected")
            print(embed)
            ctx = self.live_channel_obj
            raw = await self.getJSON(ctx)
            print(raw)
            ## print(problems, " ", percent_online)
            await self.live_channel_obj.edit(embed=embed)

    async def live_logic(self, ctx):
        raw = await self.getJSON(ctx)
        print("livelogic")
        found_count = 0
        online_count = 0
        missing_array = []
        counted_shards = 0
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
            if True:
                counted_shards += 1
                if raw[str(i)] == "CONNECTED":
                    online_count += 1
                elif raw[str(i)] in status_dict:
                    status_dict[raw[str(i)]].append(str(i))
                else:
                    missing_array.append(str(i))
        if online_count == counted_shards:
            problems = 0
            percent_online = str(100)
        else:
            problems = counted_shards - online_count
            percent_online = str(round(100 * (online_count / counted_shards), 2))
        return problems, percent_online

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
                raw = await self.fetch(session, "http://10.10.10.61:1346/shardinfo", ctx)
                ## https://status.rythmbot.co/raw for when external
                ## http://10.10.10.61:1346/shardinfo when internal
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

    def get_resolution_time(self, problems):
        time_in_minutes = str(timedelta(seconds=int(problems * (6.5 / 16))))
        return time_in_minutes

    @commands.command()
    async def livestart(self, ctx):
        embed = discord.Embed(colour=discord.Colour(0x2a60f3),
                              description="Loading Live updates...")
        embed.set_author(name="Live Rythm Status")
        embed.set_footer(text="Loading")
        embed.add_field(name="Loading", value="Loading")
        self.live_channel_obj = await ctx.send(embed=embed)
        embed = None

    @commands.command()
    async def liveend(self, ctx):
        self.live_channel_obj = None

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
        ## add commands.CommandInvokeError?

    async def info(self, ctx, cluster_choice):
        raw = await self.getJSON(ctx)
        found_count = 0
        online_count = 0
        missing_array = []
        counted_shards = 0
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
            if cluster_choice == "all" or int(math.floor(int(i) / int(math.ceil(self.shardCount / 9)))) == int(cluster_choice):
                counted_shards += 1
                if raw[str(i)] == "CONNECTED":
                    online_count += 1
                elif raw[str(i)] in status_dict:
                    status_dict[raw[str(i)]].append(str(i))
                else:
                    missing_array.append(str(i))
        if cluster_choice == "all":
            command_type = ""
        else:
            command_type = " Cluster " + cluster_choice
        if online_count == counted_shards:
            embed = discord.Embed(colour=discord.Colour(0xd0892f),
                                  description="Rythm{} is 100% Online\nThere are 0 issues".format(
                                      command_type))
            embed.set_author(name="Rythm{} Status".format(command_type))
            embed.set_footer(text="a bot by ash#0001")
            await ctx.send(embed=embed)
        else:
            if cluster_choice == "all":
                problems = counted_shards - online_count
            else:
                problems = counted_shards - online_count
            embed = discord.Embed(colour=discord.Colour(0xd0892f),
                                  description="Rythm {} is {}% Online\nThere are {} issues".format(
                                      command_type,
                                      str(round(100*(online_count / counted_shards), 2)), problems))
            embed.set_author(name="Rythm {} Status".format(command_type))
            embed.set_footer(text="a bot by ash#0001")
            for selection in status_dict:
                if len(status_dict[selection]) != 0:
                    embed.add_field(name=string_dict[selection], value=str((len(status_dict[selection]))), inline=False)
                elif len(missing_array) != 0:
                    embed.add_field(name="Data missing", value=str((len(missing_array))), inline=False)
            if problems != 0:
                embed.add_field(name="Expected Resolution Time", value=self.get_resolution_time(problems), inline=False)
            await ctx.send(embed=embed)

    def isint(test_value):
        try:
            int(test_value)
            return True
        except ValueError:
            return False

    @commands.command(aliases=["c"])
    async def cluster(self, ctx, *, cluster_choice: typing.Optional[str] = None):
        if not cluster_choice:
            await ctx.channel.send('You need to specify cluster number')
        elif not ShellCog.isint(cluster_choice):
            await ctx.channel.send('Cluster number cannot be a string')
        elif int(cluster_choice) > 9 or int(cluster_choice) < 1:
            await ctx.channel.send('Cluster number must be between 1 and 9')
        else:
            await self.info(ctx, cluster_choice)


    @commands.command(aliases=["info", "i"])
    async def status(self, ctx):
        cluster_choice = "all"
        await self.info(ctx, cluster_choice)

    @commands.command(aliases=["g"])
    async def guild(self, ctx, guild_id: int):
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
                                  str(round(100*(onlinecount / self.shardCount), 2)), problems))
        embed.set_author(name="Rythm Cluster Status")
        iterative = 0
        for j in clusters:
            if len(j) != 0:
                cluster_name = "Cluster " + str(iterative)
                embed.add_field(name=cluster_name, value=str((len(j))), inline=False)
            iterative += 1
        embed.set_footer(text="a bot by ash#0001")
        if problems != 0:
            embed.add_field(name="Expected Resolution Time", value=self.get_resolution_time(problems), inline=False)
        await ctx.send(embed=embed)



    @commands.command()
    async def check(self, ctx):
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
