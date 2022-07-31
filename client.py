from discord.ext import commands
import os
import config

if __name__ == "__main__":
    import discord

    cog_list = ['cogs.manga']

    intents = discord.Intents.default()
    intents.members = True

    bot = commands.Bot(command_prefix=config.COMMAND_PREFIX, intents=intents, help_command=None)
    [bot.load_extension(x) for x in cog_list]

    token = os.environ['BOT_TOKEN']

    bot.run(token)