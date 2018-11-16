__authors__ = 'aejb'
import discord
from discord.ext import commands
import sqlite3
import os
import subprocess
import requests
import sys
from bs4 import BeautifulSoup
import json
import math

class shellcog:

    def __init__(self, bot):
        self.bot = bot
        self.shardcount=2304

    def getstr(self, arre):
        if len(arre)>5:
            return "..."
        elif len(arre)==0:
            return ""
        else:
            arre_s=">"
            for i in arre:
                arre_s="\t"+arre_s+i+", "
            return arre_s

    @commands.command()
    async def help(self, ctx):
        await ctx.channel.send("**Command**\t\t\t\t\t\t\t**Aliases**\t\t**Description**\n`ri hello`\n`ri help`\t\t\t\t\t\t\t\tNone\t\t  This command\n`ri guild <guild_ID>`\t`g`\t\t\t\tShard and Cluster information from the given Guild ID\n`ri shard <shard_ID>`\t`s`\t\tShard and Cluster information from the given Shard ID")

    @commands.command()
    async def hello(self, ctx):
        await ctx.channel.send("oh hi")

    @commands.command(aliases=["g"])
    async def guild(self, ctx, guild_ID: int):
        url_combined = str("https://web.rythmbot.co/ajax/shard/" + str(guild_ID))
        page = requests.get(url_combined)
        python_obj = json.loads(page.text)
        shard_ID=int(python_obj["shard"])
        cluster_ID=int(python_obj["cluster"])
        embed = discord.Embed(colour=discord.Colour(0xd0892f), description="Info from Guild")
        embed.add_field(name="Guild", value=guild_ID, inline=False)
        embed.add_field(name="Shard", value=shard_ID, inline=False)
        embed.add_field(name="Cluster", value=cluster_ID, inline=False)
        rawstat = requests.get("https://status.rythmbot.co/raw")
        embed.add_field(name="Status", value=json.loads(rawstat.text)[str(shard_ID)], inline=False)
        embed.set_footer(text="a bot by ash#0001")
        await ctx.send(embed=embed)

    @commands.command(aliases=["s"])
    async def shard(self, ctx, shard_ID: int):
        embed = discord.Embed(colour=discord.Colour(0xd0892f), description="Info from Shard")
        embed.add_field(name="Shard", value=shard_ID, inline=False)
        embed.add_field(name="Cluster", value=math.floor(int(shard_ID)/int(math.ceil(self.shardcount/9))), inline=False)
        rawstat = requests.get("https://status.rythmbot.co/raw")
        embed.add_field(name="Status", value=json.loads(rawstat.text)[str(shard_ID)], inline=False)
        embed.set_footer(text="a bot by ash#0001")
        await ctx.send(embed=embed)

    @commands.command(aliases=["c"])
    async def cluster(self, ctx):
        onlinecount=0
        issues_array=[]
        #!debug rawstat = requests.get("http://cdn.dvorak.host/test.json")
        rawstat = requests.get("https://status.rythmbot.co/raw")
        raw=json.loads(rawstat.text)
        for i in raw:
            if raw[str(i)]=="CONNECTED":
                onlinecount=onlinecount+1
            else:
                shard_ID=int(i)
                cluster_ID=math.floor(int(shard_ID)/int(math.ceil(self.shardcount/9)))
                issues_array.append([shard_ID, cluster_ID])
        cluster0=[]
        cluster1=[]
        cluster2=[]
        cluster3=[]
        cluster4=[]
        cluster5=[]
        cluster6=[]
        cluster7=[]
        cluster8=[]
        cluster9=[]
        for j in issues_array:
            if (j[1])==0:
                cluster0.append(j)
            if (j[1])==1:
                cluster1.append(j)
            if (j[1])==2:
                cluster2.append(j)
            if (j[1])==3:
                cluster3.append(j)
            if (j[1])==4:
                cluster4.append(j)
            if (j[1])==5:
                cluster5.append(j)
            if (j[1])==6:
                cluster6.append(j)
            if (j[1])==7:
                cluster7.append(j)
            if (j[1])==8:
                cluster8.append(j)
            if (j[1])==9:
                cluster9.append(j)
        problems=self.shardcount-onlinecount
        embed = discord.Embed(colour=discord.Colour(0xd0892f), description="Rythm is {}% Online\nThere are {} issues".format(str(round(((onlinecount)/self.shardcount), 1)*100), problems))
        embed.set_author(name="Rythm Cluster Status")
        if len(cluster0)!=0:
            embed.add_field(name="Cluster 0", value=(len(cluster0)), inline=False)
        if len(cluster1)!=0:
            embed.add_field(name="Cluster 1", value=(len(cluster1)), inline=False)
        if len(cluster2)!=0:
            embed.add_field(name="Cluster 2", value=(len(cluster2)), inline=False)
        if len(cluster3)!=0:
            embed.add_field(name="Cluster 3", value=(len(cluster3)), inline=False)
        if len(cluster4)!=0:
            embed.add_field(name="Cluster 4", value=(len(cluster4)), inline=False)
        if len(cluster5)!=0:
            embed.add_field(name="Cluster 5", value=(len(cluster5)), inline=False)
        if len(cluster6)!=0:
            embed.add_field(name="Cluster 6", value=(len(cluster6)), inline=False)
        if len(cluster7)!=0:
            embed.add_field(name="Cluster 7", value=(len(cluster7)), inline=False)
        if len(cluster8)!=0:
            embed.add_field(name="Cluster 8", value=(len(cluster8)), inline=False)
        if len(cluster9)!=0:
            embed.add_field(name="Cluster 9", value=(len(cluster9)), inline=False)
        embed.set_footer(text="a bot by ash#0001")
        await ctx.send(embed=embed)

    @commands.command(aliases=["info", "i"])
    async def status(self, ctx):
        onlinecount=0
        initi=[]
        initd=[]
        log=[]
        webs=[]
        ident=[]
        awaiting=[]
        load=[]
        recon=[]
        attempt=[]
        waitcon=[]
        queue=[]
        missing=[]
        rawstat = requests.get("https://status.rythmbot.co/raw")
        #!debug rawstat = requests.get("http://cdn.dvorak.host/test.json")
        raw=json.loads(rawstat.text)
        for i in raw:
            if raw[str(i)]=="CONNECTED":
                onlinecount=onlinecount+1
            elif raw[str(i)]=="INITIALIZING":
                initi.append(str(i))
            elif raw[str(i)]=="INITIALIZED":
                initd.append(str(i))
            elif raw[str(i)]=="LOGGING_IN":
                log.append(str(i))
            elif raw[str(i)]=="CONNECTING_TO_WEBSOCKET":
                webs.append(str(i))
            elif raw[str(i)]=="IDENTIFYING_SESSION":
                ident.append(str(i))
            elif raw[str(i)]=="AWAITING_LOGIN_CONFIRMATION":
                awaiting.append(str(i))
            elif raw[str(i)]=="LOADING_SUBSYSTEMS":
                load.append(str(i))
            elif raw[str(i)]=="RECONNECTING":
                recon.append(str(i))
            elif raw[str(i)]=="ATTEMPTING_TO_RECONNECT":
                attempt.append(str(i))
            elif raw[str(i)]=="WAITING_TO_RECONNECT":
                waitcon.append(str(i))
            elif raw[str(i)]=="RECONNECT_QUEUED":
                queue.append(str(i))
            else:
                missing.append(str(i))
        if onlinecount==self.shardcount:
            embed = discord.Embed(colour=discord.Colour(0xd0892f), description="Rythm is 100% Online\nThere are 0 issues")
            embed.set_author(name="Rythm Status")
            embed.set_footer(text="a bot by ash#0001")
            await ctx.send(embed=embed)

        else:
            problems=self.shardcount-onlinecount
            embed = discord.Embed(colour=discord.Colour(0xd0892f), description="Rythm is {}% Online\nThere are {} issues".format(str(round(((onlinecount)/self.shardcount), 1)*100), problems))
            embed.set_author(name="Rythm Status")
            embed.set_footer(text="a bot by ash#0001")
            if len(queue) != 0:
                embed.add_field(name="Reconnect queue", value=(len(queue)), inline=False)
            if len(waitcon) != 0:
                embed.add_field(name="Waiting to reconnect", value=(len(waitcon)), inline=False)
            if len(load) != 0:
                embed.add_field(name="Loading subsystems", value=(len(load)), inline=False)
            if len(awaiting) != 0:
                embed.add_field(name="Awaiting confirmation", value=(len(awaiting)), inline=False)
            if len(initi) != 0:
                embed.add_field(name="Initialising", value=(len(initi)), inline=False)
            if len(initd) != 0:
                embed.add_field(name="Initialised", value=(len(initd)), inline=False)
            if len(log) != 0:
                embed.add_field(name="Logging in", value=(len(log)), inline=False)
            if len(webs) != 0:
                embed.add_field(name="Connecting to websocket", value=(len(webs)), inline=False)
            if len(ident) != 0:
                embed.add_field(name="Identifying", value=(len(ident)), inline=False)
            if len(recon) != 0:
                embed.add_field(name="Reconnecting", value=(len(recon)), inline=False)
            if len(attempt) != 0:
                embed.add_field(name="Attempting to reconnect", value=(len(attempt)), inline=False)
            if len(missing) != 0:
                embed.add_field(name="Data missing", value=(len(missing)), inline=False)
            await ctx.send(embed=embed)

def setup(bot):
    bot.remove_command("help")
    bot.add_cog(shellcog(bot))
