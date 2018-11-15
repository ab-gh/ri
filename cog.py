__authors__ = 'electric-blue-green'
__license__ = 'MIT'
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
    async def hello(self, ctx):
        await ctx.channel.send("oh hi")

    @commands.command()
    async def guild(self, ctx, guild_ID: int):
        url_combined = str("https://web.rythmbot.co/ajax/shard/" + guild_ID)
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
        #print(f"\nshard:\t\t{shard_ID}\ncluster:\t{cluster_ID}\n")
        #print(f"{shard_ID}:", json.loads(rawstat.text)[str(shard_ID)])
        await ctx.send(embed=embed)



    @commands.command()
    async def cluster(self, ctx):
        shardcount=2304
        onlinecount=0
        issues_array=[]



        #### change this!!!
        rawstat = requests.get("http://cdn.dvorak.host/test.json")
        ####



        raw=json.loads(rawstat.text)
        for i in raw:
            if raw[str(i)]=="CONNECTED":
                onlinecount=onlinecount+1
            else:
                shard_ID=int(i)
                cluster_ID=math.floor(int(shard_ID)/int(math.ceil(shardcount/9)))
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
            ###
        problems=shardcount-onlinecount
        embed = discord.Embed(colour=discord.Colour(0xd0892f), description="Rythm is {}% Online\nThere are {} issues".format(str(round(((onlinecount)/shardcount), 1)*100), problems))

        #print("\nTotal Issues\t", len(issues_array))
        if len(cluster0)!=0:
            embed.add_field(name="Cluster 0", value=(len(cluster0)), inline=False)
            #print("rc 0 Issues\t", "{0:0=3d}".format(len(cluster0)))
        if len(cluster1)!=0:
            embed.add_field(name="Cluster 1", value=(len(cluster1)), inline=False)
            #print("rc 1 Issues\t", "{0:0=3d}".format(len(cluster1)))
        if len(cluster2)!=0:
            embed.add_field(name="Cluster 2", value=(len(cluster2)), inline=False)
            #print("rc 2 Issues\t", "{0:0=3d}".format(len(cluster2)))
        if len(cluster3)!=0:
            embed.add_field(name="Cluster 3", value=(len(cluster3)), inline=False)
            #print("rc 3 Issues\t", "{0:0=3d}".format(len(cluster3)))
        if len(cluster4)!=0:
            embed.add_field(name="Cluster 4", value=(len(cluster4)), inline=False)
            #print("rc 4 Issues\t", "{0:0=3d}".format(len(cluster4)))
        if len(cluster5)!=0:
            embed.add_field(name="Cluster 5", value=(len(cluster5)), inline=False)
            #print("rc 5 Issues\t", "{0:0=3d}".format(len(cluster5)))
        if len(cluster6)!=0:
            embed.add_field(name="Cluster 6", value=(len(cluster6)), inline=False)
            #print("rc 6 Issues\t", "{0:0=3d}".format(len(cluster6)))
        if len(cluster7)!=0:
            embed.add_field(name="Cluster 7", value=(len(cluster7)), inline=False)
            #print("rc 7 Issues\t", "{0:0=3d}".format(len(cluster7)))
        if len(cluster8)!=0:
            embed.add_field(name="Cluster 8", value=(len(cluster8)), inline=False)
            #print("rc 8 Issues\t", "{0:0=3d}".format(len(cluster8)))
        if len(cluster9)!=0:
            embed.add_field(name="Cluster 9", value=(len(cluster9)), inline=False)
            #print("rc 9 Issues\t", "{0:0=3d}".format(len(cluster9)))
        await ctx.send(embed=embed)


    @commands.command()
    async def status(self, ctx):
        shardcount=2304
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
        #rawstat = requests.get("https://status.rythmbot.co/raw")
        rawstat = requests.get("http://cdn.dvorak.host/test.json")
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
        if onlinecount==shardcount:

            embed = discord.Embed(colour=discord.Colour(0xd0892f), description="Rythm is Online")

            embed.set_author(name="Rythm Status")
            embed.set_footer(text="a bot by ash#0001")

            await ctx.send(embed=embed)


        else:
            #print("Rythm is ", round(((onlinecount)/shardcount), 1)*100, "% online")
            problems=shardcount-onlinecount
            #print("------------------------------")
            #print("By issue\n")
            #print("Total Issues\t", problems)
            embed = discord.Embed(colour=discord.Colour(0xd0892f), description="Rythm is {}% Online\nThere are {} issues".format(str(round(((onlinecount)/shardcount), 1)*100), problems))
            embed.set_author(name="Rythm Status")
            embed.set_footer(text="a bot by ash#0001")

            if len(queue) != 0:
                embed.add_field(name="Reconnect queue", value=(len(queue)), inline=False)
                #print("In recon queue\t", "{0:0=3d}".format(len(queue)), getstr(queue))
            if len(waitcon) != 0:
                #print("Wait to recon\t", "{0:0=3d}".format(len(waitcon)), self.getstr(waitcon))
                embed.add_field(name="Waiting to reconnect", value=(len(waitcon)), inline=False)
            if len(load) != 0:
                #print("Loading subs\t", "{0:0=3d}".format(len(load)), self.getstr(load))
                embed.add_field(name="Loading subsystems", value=(len(load)), inline=False)
            if len(awaiting) != 0:
                #print("Awaiting conf\t", "{0:0=3d}".format(len(awaiting)), self.getstr(awaiting))
                embed.add_field(name="Awaiting confirmation", value=(len(awaiting)), inline=False)
            if len(initi) != 0:
                #print("Initialising\t\t", "{0:0=3d}".format(len(initi)), self.getstr(initi))
                embed.add_field(name="Initialising", value=(len(initi)), inline=False)
            if len(initd) != 0:
                #print("Initialised\t\t", "{0:0=3d}".format(len(initd)), self.getstr(initd))
                embed.add_field(name="Initialised", value=(len(initd)), inline=False)
            if len(log) != 0:
                #print("Logging in\t", "{0:0=3d}".format(len(log)), "\t", self.getstr(log))
                embed.add_field(name="Logging in", value=(len(log)), inline=False)
            if len(webs) != 0:
                #print("Connect to webs", "{0:0=3d}".format(len(webs)), self.getstr(webs))
                embed.add_field(name="Connecting to websocket", value=(len(webs)), inline=False)
            if len(ident) != 0:
                #print("Identifying\t\t", "{0:0=3d}".format(len(ident)), self.getstr(ident))
                embed.add_field(name="Identifying", value=(len(ident)), inline=False)
            if len(recon) != 0:
                #print("Reconnecting\t\t", "{0:0=3d}".format(len(recon)), self.getstr(recon))
                embed.add_field(name="Reconnecting", value=(len(recon)), inline=False)
            if len(attempt) != 0:
                #print("Attempt to reconn", "{0:0=3d}".format(len(attempt)), self.getstr(attempt))
                embed.add_field(name="Attempting to reconnect", value=(len(attempt)), inline=False)
            if len(missing) != 0:
                #print("Data missing", "{0:0=3d}".format(len(missing)), self.getstr(missing))
                embed.add_field(name="Data missing", value=(len(missing)), inline=False)
            await ctx.send(embed=embed)




def setup(bot):
    bot.add_cog(shellcog(bot))
