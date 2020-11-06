import discord
from discord.ext import commands
from discord.ext.commands import when_mentioned_or

from core import constants

bot = commands.Bot(
    activity=discord.Game(name="Pwning The Jewels"),
    case_insensitive=False,
    command_prefix=when_mentioned_or(constants.Bot.prefix),
    help_command=None,
    max_messages=10000
)

if __name__ == "__main__":
    # Import commands.py in order to use commands
    bot.load_extension("core.commands")

    bot.run(constants.Bot.token)
