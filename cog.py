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

    @commands.command()
    async def hello(self, ctx): # by proxy of below (status), v4 fixed this line
        await ctx.channel.send("oh hi")

    @commands.command()
    async def status(self, ctx): # v4 fixed this line
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
        rawstat = requests.get("https://status.rythmbot.co/raw")
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
            embed = discord.Embed(colour=discord.Colour(0xd0892f), description="Rythm is {}% Online".format(str(round(((onlinecount)/shardcount), 1)*100)))
            embed.set_author(name="Rythm Status")
            embed.set_footer(text="a bot by ash#0001")
            #print("Rythm is ", round(((onlinecount)/shardcount), 1)*100, "% online")
            print(onlinecount, "\t Online")
            problems=shardcount-onlinecount
            print("------------------------------")
            print("By issue\n")
            print("Total Issues\t", problems)
            if len(queue) != 0:
                embed.add_field(name="Reconnect queue", value=(len(queue)))
                #print("In recon queue\t", "{0:0=3d}".format(len(queue)), getstr(queue))
            if len(waitcon) != 0:
                print("Wait to recon\t", "{0:0=3d}".format(len(waitcon)), getstr(waitcon))
            if len(load) != 0:
                print("Loading subs\t", "{0:0=3d}".format(len(load)), getstr(load))
            if len(awaiting) != 0:
                print("Awaiting conf\t", "{0:0=3d}".format(len(awaiting)), getstr(awaiting))
            if len(initi) != 0:
                print("Initialising\t\t", "{0:0=3d}".format(len(initi)), getstr(initi))
            if len(initd) != 0:
                print("Initialised\t\t", "{0:0=3d}".format(len(initd)), getstr(initd))
            if len(log) != 0:
                print("Logging in\t", "{0:0=3d}".format(len(log)), "\t", getstr(log))
            if len(webs) != 0:
                print("Connect to webs", "{0:0=3d}".format(len(webs)), getstr(webs))
            if len(ident) != 0:
                print("Identifying\t\t", "{0:0=3d}".format(len(ident)), getstr(ident))
            if len(recon) != 0:
                print("Reconnecting\t\t", "{0:0=3d}".format(len(recon)), getstr(recon))
            if len(attempt) != 0:
                print("Attempt to reconn", "{0:0=3d}".format(len(attempt)), getstr(attempt))
            if len(missing) != 0:
                print("Data missing", "{0:0=3d}".format(len(missing)), getstr(missing))
            await ctx.send(embed=embed)
        print("------------------------------")
        print("By cluster")
        info_from_cluster(shardcount)



def setup(bot):
    bot.add_cog(shellcog(bot)) # v4 also fixed this line
