import aiosqlite
import discord
from discord.ext import commands
from discord.ext.commands import when_mentioned_or

from core import constants, rss, google_alerts, reddit, twitter, youtube

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
        # Create general RSS related tables:
        await database.execute(f"CREATE TABLE IF NOT EXISTS general_rss_links(url TEXT)")
        await database.execute(f"CREATE TABLE IF NOT EXISTS general_rss_posts(id TEXT, title TEXT, url TEXT)")

        # Create Google Alerts RSS related tables:
        await database.execute(f"CREATE TABLE IF NOT EXISTS google_alerts_links(url TEXT, keyword TEXT)")
        await database.execute(f"CREATE TABLE IF NOT EXISTS google_alerts_posts(id TEXT, title TEXT, url TEXT)")

        # Create Reddit related tables:
        await database.execute(f"CREATE TABLE IF NOT EXISTS reddit_subreddits(subreddit TEXT)")
        await database.execute(f"CREATE TABLE IF NOT EXISTS reddit_posts(id TEXT, subreddit TEXT, author TEXT, title TEXT, url TEXT)")

        # Create Twitter related tables:
        await database.execute(f"CREATE TABLE IF NOT EXISTS twitter_usernames(username TEXT, retweets INT)")
        await database.execute(f"CREATE TABLE IF NOT EXISTS twitter_tweets(id INTEGER, user TEXT, text TEXT, url TEXT)")

        # Create Youtube related tables
        await database.execute(f"CREATE TABLE IF NOT EXISTS youtube_channels(channel_id TEXT, channel_name TEXT)")
        await database.execute(f"CREATE TABLE IF NOT EXISTS youtube_videos(channel_id TEXT, channel_name TEXT, video_id TEXT, title TEXT, url TEXT)")

    # Start RSS monitoring
    rss_monitor = rss.RSS(bot)
    rss_monitor.monitor_rss.start()

    # Start Google Alerts monitoring
    alert_monitor = google_alerts.Google_Alerts(bot)
    alert_monitor.monitor_alerts.start()

    # Start Reddit monitoring
    reddit_monitor = reddit.Reddit(bot)
    reddit_monitor.monitor_subreddit.start()

    # Start Twitter monitoring
    twitter_monitor = twitter.Twitter(bot)
    twitter_monitor.monitor_tweets.start()

    # # Start Youtube monitoring
    youtube_monitor = youtube.Youtube(bot)
    youtube_monitor.monitor_videos.start()


if __name__ == "__main__":
    # Import commands.py in order to use commands
    bot.load_extension("core.commands")

    bot.run(constants.Bot.token)
