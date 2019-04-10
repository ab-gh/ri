__authors__ = 'aejb'

## requires d.py 1.0
## requires python3.6
import discord
from discord.ext import commands
import traceback
import sys

initial_extensions = ['cog']


def gettoken():
    token_file = open("token.txt", "r")
    token_string = token_file.read()
    token_token = token_string.split("\n")
    bot_token = str(token_token[0])
    return bot_token


bot_token = gettoken()

description = "use ri help"
bot = commands.Bot(command_prefix=["ri "], description=description)

if __name__ == '__main__':
    for extension in initial_extensions:
        # noinspection PyBroadException
        try:
            bot.load_extension(extension)
        except Exception as e:
            print("Failed to load" + extension, file=sys.stderr)
            traceback.print_exc()


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(bot_token)
