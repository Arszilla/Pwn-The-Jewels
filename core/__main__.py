import sqlite3

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


def connect(database):
    connection = None
    try:
        connection = sqlite3.connect(database)
        cursor = connection.cursor()

        tables = list(constants.Guild.channels.keys())
        tables.remove("reminders")
        # # Create tables
        for table in tables:
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {table}(id INTEGER, url TEXT)")


    except sqlite3.Error as error:
        print(error)

    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
    # Import commands.py in order to use commands
    bot.load_extension("core.commands")

    connect(constants.Database.name)
    bot.run(constants.Bot.token)
