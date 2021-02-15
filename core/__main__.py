import aiosqlite
import discord
from discord.ext import commands
from discord.ext.commands import when_mentioned_or

from core import constants, reddit

bot = commands.Bot(
    activity=discord.Game(name="Pwning The Jewels"),
    case_insensitive=False,
    command_prefix=when_mentioned_or(constants.Bot.prefix),
    help_command=None,
    max_messages=10000
)


# Runs this function once the bot is ready.
@bot.event
async def on_ready():
    """
    The database here will be used to store the items to be tracked.
    Upon running the bot for the first time, the database and its tables will be created.
    """
    async with aiosqlite.connect(constants.Database.name) as database:
        # Create Reddit related tables
        await database.execute(f"CREATE TABLE IF NOT EXISTS reddit_subreddits(subreddit TEXT)")
        await database.execute(f"CREATE TABLE IF NOT EXISTS reddit_posts(id TEXT, subreddit TEXT, author TEXT, title TEXT, url TEXT)")

    # Start the Reddit monitoring
    reddit_monitor = reddit.Reddit(bot)
    reddit_monitor.monitor_subreddit.start()


if __name__ == "__main__":
    # Import commands.py in order to use commands
    bot.load_extension("core.commands")

    bot.run(constants.Bot.token)
