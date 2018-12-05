__authors__ = 'aejb'
import discord
from discord.ext import commands
import requests
import json
import math
import datetime


class ShellCog:

    def __init__(self, bot):
        self.bot = bot
        self.shardCount = 2304

    @commands.command()
    async def help(self, ctx):
        await ctx.channel.send("**Command**\t\t\t\t\t\t\t**Aliases**\t\t**Description**\n`ri hello`\n`ri "
                               "help`\t\t\t\t\t\t\t\tNone\t\t  This command\n`ri guild <guild_ID>`\t`g`\t\t\t\t  "
                               "Shard and Cluster information from the given Guild ID\n`ri shard "
                               "<shard_ID>`\t`s`\t\t\t\t  Shard and Cluster information from the given Shard ID\n`ri "
                               "cluster`\t\t\t\t\t\t `c`\t\t\t\t  Information on shard issues sorted by cluster\n`ri "
                               "status`\t\t\t\t\t\t   `info, i`\t Information on shard issues by issue type")

    @commands.command()
    async def hello(self, ctx):
        await ctx.channel.send("oh hi")

    @commands.command(alises="ci")
    async def clusterinfo(self, ctx, cluster_choice: int):
        onlinecount = 0
        initi = []
        initd = []
        log = []
        webs = []
        ident = []
        awaiting = []
        load = []
        recon = []
        attempt = []
        waitcon = []
        queue = []
        missing = []
        raw_stat = requests.get("http://cdn.dvorak.host/test.json")
        # raw_stat = requests.get("https://status.rythmbot.co/raw")
        raw = json.loads(raw_stat.text)
        for i in raw:
           if math.floor(int(shard_id) / int(math.ceil(self.shardCount / 9))) == cluster_choice:
               if raw[str(i)] == "CONNECTED":
                   onlinecount = onlinecount + 1
               elif raw[str(i)] == "INITIALIZING":
                   initi.append(str(i))
               elif raw[str(i)] == "INITIALIZED":
                   initd.append(str(i))
               elif raw[str(i)] == "LOGGING_IN":
                   log.append(str(i))
               elif raw[str(i)] == "CONNECTING_TO_WEBSOCKET":
                   webs.append(str(i))
               elif raw[str(i)] == "IDENTIFYING_SESSION":
                   ident.append(str(i))
               elif raw[str(i)] == "AWAITING_LOGIN_CONFIRMATION":
                   awaiting.append(str(i))
               elif raw[str(i)] == "LOADING_SUBSYSTEMS":
                   load.append(str(i))
               elif raw[str(i)] == "RECONNECTING":
                   recon.append(str(i))
               elif raw[str(i)] == "ATTEMPTING_TO_RECONNECT":
                   attempt.append(str(i))
               elif raw[str(i)] == "WAITING_TO_RECONNECT":
                   waitcon.append(str(i))
               elif raw[str(i)] == "RECONNECT_QUEUED":
                   queue.append(str(i))
               else:
                   missing.append(str(i))
           else:
               return
        if onlinecount == self.shardCount:
            embed = discord.Embed(colour=discord.Colour(0xd0892f),
                                  description="Rythm Cluster {}% is 100% Online\nThere are 0 issues".format(cluster_choice))
            embed.set_author(name="Rythm Cluster {}% Status".format(cluster_choice))
            embed.set_footer(text="a bot by ash#0001")
            await ctx.send(embed=embed)
        else:
            problems = self.shardCount - onlinecount
            embed = discord.Embed(colour=discord.Colour(0xd0892f),
                                  description="Rythm Cluster {}% is {}% Online\nThere are {} issues".format(cluster_choice,
                                      str(round((onlinecount / self.shardCount), 1) * 100), problems))
            embed.set_author(name="Rythm Cluster {}% Status".format(cluster_choice))
            embed.set_footer(text="a bot by ash#0001")
            if len(queue) != 0:
                embed.add_field(name="Reconnect queue", value=str((len(queue))), inline=False)
            if len(waitcon) != 0:
                embed.add_field(name="Waiting to reconnect", value=str((len(waitcon))), inline=False)
            if len(load) != 0:
                embed.add_field(name="Loading subsystems", value=str((len(load))), inline=False)
            if len(awaiting) != 0:
                embed.add_field(name="Awaiting confirmation", value=str((len(awaiting))), inline=False)
            if len(initi) != 0:
                embed.add_field(name="Initialising", value=str((len(initi))), inline=False)
            if len(initd) != 0:
                embed.add_field(name="Initialised", value=str((len(initd))), inline=False)
            if len(log) != 0:
                embed.add_field(name="Logging in", value=str((len(log))), inline=False)
            if len(webs) != 0:
                embed.add_field(name="Connecting to websocket", value=str((len(webs))), inline=False)
            if len(ident) != 0:
                embed.add_field(name="Identifying", value=str((len(ident))), inline=False)
            if len(recon) != 0:
                embed.add_field(name="Reconnecting", value=str((len(recon))), inline=False)
            if len(attempt) != 0:
                embed.add_field(name="Attempting to reconnect", value=str((len(attempt))), inline=False)
            if len(missing) != 0:
                embed.add_field(name="Data missing", value=str((len(missing))), inline=False)
            await ctx.send(embed=embed)


    @commands.command(aliases=["g"])
    async def guild(self, ctx, guild_id: int):
        url_combined = str("https://web.rythmbot.co/ajax/shard/" + str(guild_id))
        page = requests.get(url_combined)
        python_obj = json.loads(page.text)
        shard_id = int(python_obj["shard"])
        cluster_id = int(python_obj["cluster"])
        embed = discord.Embed(colour=discord.Colour(0xd0892f), description="Info from Guild")
        embed.add_field(name="Guild", value=str(guild_id), inline=False)
        embed.add_field(name="Shard", value=str(shard_id), inline=False)
        embed.add_field(name="Cluster", value=str(cluster_id), inline=False)
        raw_stat = requests.get("https://status.rythmbot.co/raw")
        embed.add_field(name="Status", value=json.loads(raw_stat.text)[str(shard_id)], inline=False)
        embed.set_footer(text="a bot by ash#0001")
        await ctx.send(embed=embed)

    @commands.command(aliases=["s"])
    async def shard(self, ctx, shard_id: int):
        embed = discord.Embed(colour=discord.Colour(0xd0892f), description="Info from Shard")
        embed.add_field(name="Shard", value=str(shard_id), inline=False)
        embed.add_field(name="Cluster", value=str(math.floor(int(shard_id) / int(math.ceil(self.shardCount / 9)))),
                        inline=False)
        raw_stat = requests.get("https://status.rythmbot.co/raw")
        embed.add_field(name="Status", value=json.loads(raw_stat.text)[str(shard_id)], inline=False)
        embed.set_footer(text="a bot by ash#0001")
        await ctx.send(embed=embed)

    @commands.command(aliases=["c"])
    async def cluster(self, ctx):
        onlinecount = 0
        issues_array = []
        raw_stat = requests.get("http://cdn.dvorak.host/test.json")
        #raw_stat = requests.get("https://status.rythmbot.co/raw")
        raw = json.loads(raw_stat.text)
        for i in raw:
            if raw[str(i)] == "CONNECTED":
                onlinecount = onlinecount + 1
            else:
                shard_id = int(i)
                cluster_id = math.floor(int(shard_id) / int(math.ceil(self.shardCount / 9)))
                issues_array.append([shard_id, cluster_id])
        cluster0 = []
        cluster1 = []
        cluster2 = []
        cluster3 = []
        cluster4 = []
        cluster5 = []
        cluster6 = []
        cluster7 = []
        cluster8 = []
        cluster9 = []
        for j in issues_array:
            if (j[1]) == 0:
                cluster0.append(j)
            if (j[1]) == 1:
                cluster1.append(j)
            if (j[1]) == 2:
                cluster2.append(j)
            if (j[1]) == 3:
                cluster3.append(j)
            if (j[1]) == 4:
                cluster4.append(j)
            if (j[1]) == 5:
                cluster5.append(j)
            if (j[1]) == 6:
                cluster6.append(j)
            if (j[1]) == 7:
                cluster7.append(j)
            if (j[1]) == 8:
                cluster8.append(j)
            if (j[1]) == 9:
                cluster9.append(j)
        problems = self.shardCount - onlinecount
        embed = discord.Embed(colour=discord.Colour(0xd0892f),
                              description="Rythm is {}% Online\nThere are {} issues".format(
                                  str(round((onlinecount / self.shardCount), 1) * 100), problems))
        embed.set_author(name="Rythm Cluster Status")
        if len(cluster0) != 0:
            embed.add_field(name="Cluster 0", value=str((len(cluster0))), inline=False)
        if len(cluster1) != 0:
            embed.add_field(name="Cluster 1", value=str((len(cluster1))), inline=False)
        if len(cluster2) != 0:
            embed.add_field(name="Cluster 2", value=str((len(cluster2))), inline=False)
        if len(cluster3) != 0:
            embed.add_field(name="Cluster 3", value=str((len(cluster3))), inline=False)
        if len(cluster4) != 0:
            embed.add_field(name="Cluster 4", value=str((len(cluster4))), inline=False)
        if len(cluster5) != 0:
            embed.add_field(name="Cluster 5", value=str((len(cluster5))), inline=False)
        if len(cluster6) != 0:
            embed.add_field(name="Cluster 6", value=str((len(cluster6))), inline=False)
        if len(cluster7) != 0:
            embed.add_field(name="Cluster 7", value=str((len(cluster7))), inline=False)
        if len(cluster8) != 0:
            embed.add_field(name="Cluster 8", value=str((len(cluster8))), inline=False)
        if len(cluster9) != 0:
            embed.add_field(name="Cluster 9", value=str((len(cluster9))), inline=False)
        embed.set_footer(text="a bot by ash#0001")
        time_to_seconds = int(problems * 6.5)
        time_in_minutes = str(datetime.timedelta(seconds=time_to_seconds))
        embed.add_field(name="Expected Resolution Time", value=time_in_minutes, inline=False)
        await ctx.send(embed=embed)

    # RYTHM INFO

    @commands.command(aliases=["info", "i"])
    async def status(self, ctx):
        onlinecount = 0
        initi = []
        initd = []
        log = []
        webs = []
        ident = []
        awaiting = []
        load = []
        recon = []
        attempt = []
        waitcon = []
        queue = []
        missing = []
        #raw_stat = requests.get("https://status.rythmbot.co/raw")
        raw_stat = requests.get("http://cdn.dvorak.host/test.json")
        raw = json.loads(raw_stat.text)
        for i in raw:
            if raw[str(i)] == "CONNECTED":
                onlinecount = onlinecount + 1
            elif raw[str(i)] == "INITIALIZING":
                initi.append(str(i))
            elif raw[str(i)] == "INITIALIZED":
                initd.append(str(i))
            elif raw[str(i)] == "LOGGING_IN":
                log.append(str(i))
            elif raw[str(i)] == "CONNECTING_TO_WEBSOCKET":
                webs.append(str(i))
            elif raw[str(i)] == "IDENTIFYING_SESSION":
                ident.append(str(i))
            elif raw[str(i)] == "AWAITING_LOGIN_CONFIRMATION":
                awaiting.append(str(i))
            elif raw[str(i)] == "LOADING_SUBSYSTEMS":
                load.append(str(i))
            elif raw[str(i)] == "RECONNECTING":
                recon.append(str(i))
            elif raw[str(i)] == "ATTEMPTING_TO_RECONNECT":
                attempt.append(str(i))
            elif raw[str(i)] == "WAITING_TO_RECONNECT":
                waitcon.append(str(i))
            elif raw[str(i)] == "RECONNECT_QUEUED":
                queue.append(str(i))
            else:
                missing.append(str(i))
        if onlinecount == self.shardCount:
            embed = discord.Embed(colour=discord.Colour(0xd0892f),
                                  description="Rythm is 100% Online\nThere are 0 issues")
            embed.set_author(name="Rythm Status")
            embed.set_footer(text="a bot by ash#0001")
            await ctx.send(embed=embed)

        else:
            problems = self.shardCount - onlinecount
            embed = discord.Embed(colour=discord.Colour(0xd0892f),
                                  description="Rythm is {}% Online\nThere are {} issues".format(
                                      str(round((onlinecount / self.shardCount), 1) * 100), problems))
            embed.set_author(name="Rythm Status")
            embed.set_footer(text="a bot by ash#0001")
            if len(queue) != 0:
                embed.add_field(name="Reconnect queue", value=str((len(queue))), inline=False)
            if len(waitcon) != 0:
                embed.add_field(name="Waiting to reconnect", value=str((len(waitcon))), inline=False)
            if len(load) != 0:
                embed.add_field(name="Loading subsystems", value=str((len(load))), inline=False)
            if len(awaiting) != 0:
                embed.add_field(name="Awaiting confirmation", value=str((len(awaiting))), inline=False)
            if len(initi) != 0:
                embed.add_field(name="Initialising", value=str((len(initi))), inline=False)
            if len(initd) != 0:
                embed.add_field(name="Initialised", value=str((len(initd))), inline=False)
            if len(log) != 0:
                embed.add_field(name="Logging in", value=str((len(log))), inline=False)
            if len(webs) != 0:
                embed.add_field(name="Connecting to websocket", value=str((len(webs))), inline=False)
            if len(ident) != 0:
                embed.add_field(name="Identifying", value=str((len(ident))), inline=False)
            if len(recon) != 0:
                embed.add_field(name="Reconnecting", value=str((len(recon))), inline=False)
            if len(attempt) != 0:
                embed.add_field(name="Attempting to reconnect", value=str((len(attempt))), inline=False)
            if len(missing) != 0:
                embed.add_field(name="Data missing", value=str((len(missing))), inline=False)
            time_to_seconds = int(problems * 6.5)
            time_in_minutes = str(datetime.timedelta(seconds=time_to_seconds))
            embed.add_field(name="Expected Resolution Time", value=time_in_minutes, inline=False)
            await ctx.send(embed=embed)


def setup(bot):
    bot.remove_command("help")
    bot.add_cog(ShellCog(bot))
