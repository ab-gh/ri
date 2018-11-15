__authors__ = 'electric-blue-green'
__license__ = 'MIT'
import discord
from discord.ext import commands
import sqlite3
import os
import subprocess

class shellcog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(ctx):
        await ctx.channel.send("oh hi")


def setup(bot):
    bot.add_cog(shellcog)
