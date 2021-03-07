from asyncio import sleep

import discord
from discord.ext import commands

from core import constants
from core.monitoring import (RSS, Google_Alerts, Reddit, Telegram, Twitter,
                             YouTube)


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, context):
        """
        The typical help command for the bot. The actual print message 
        has been overwritten to this in __main__.py
        """

        embed = discord.Embed(
            title="Available Commands",
            type="rich",
            color=0xBA1070
        )
        embed.add_field(
            name="help",
            value="Displays this menu.",
            inline=False
        )
        embed.add_field(
            name="clear",
            value="Clears a given amount of messages from the channel the command was invoked in.\n"
                  "Example usage:  `$clear <amount>`",
            inline=False
        )
        embed.add_field(
            name="addrss",
            value="Add a RSS feed to the database.\n"
                  "Example usage: `$addrss <url>`",
            inline=False
        )
        embed.add_field(
            name="removerss",
            value="Remove a RSS feed from the database.\n"
                  "Example usage: `$removerss <url>`",
            inline=False
        )
        embed.add_field(
            name="addalert",
            value="Add a Google Alerts RSS feed to the database.\n"
                  "Example usage: `$addalert <url>`",
            inline=False
        )
        embed.add_field(
            name="removealert",
            value="Remove a Google Alerts RSS feed from the database.\n"
                  "Example usage: `$removealert <url>`",
            inline=False
        )
        embed.add_field(
            name="addsubreddit",
            value="Add a subreddit to the database.\n"
                  "The `/r/` should **NOT** be included.\n"
                  "Example usage: `$addsubreddit <subreddit-name>`",
            inline=False
        )
        embed.add_field(
            name="removesubreddit",
            value="Remove a subreddit from the database.\n"
                  "The `/r/` should **NOT** be included.\n"
                  "Example usage: `$addsubreddit <subreddit-name>`",
            inline=False
        )
        embed.add_field(
            name="addtelegram",
            value="Add a Telegram RSS feed to the database.\n"
                  "Example usage: `$addtelegram <url>`",
            inline=False
        )
        embed.add_field(
            name="removetelegram",
            value="Remove a Telegram RSS feed from the database.\n"
                  "Example usage: `$removetelegram <url>`",
            inline=False
        )
        embed.add_field(
            name="addtweeter",
            value="Add a Twitter user to the database.\n"
                  "The `@` should **NOT** be included.\n"
                  "Example usage: `$addtweeter <username>`",
            inline=False
        )
        embed.add_field(
            name="removetweeter",
            value="Remove a Twitter user from the database.\n"
                  "The `@` should **NOT** be included.\n"
                  "Example usage: `$removetweeter <username>`",
            inline=False
        )
        embed.add_field(
            name="enablerts",
            value="Enable monitoring for retweets for a given username in the database.\n"
                  "By default this is disabled.\n"
                  "The `@` should **NOT** be included.\n"
                  "Example usage: `$enablerts <username>`",
            inline=False
        )
        embed.add_field(
            name="disablerts",
            value="Disable monitoring for retweets for a given username in the database.\n"
                  "The `@` should **NOT** be included.\n"
                  "Example usage: `$disablerts <username>`",
            inline=False
        )
        embed.add_field(
            name="addchannel",
            value="Add a YouTube channel to the database.\n"
                  "Example usage: `$addchannel <channel-url>`",
            inline=False
        )
        embed.add_field(
            name="removechannel",
            value="Remove a YouTube channel from the database.\n"
                  "Example usage: `$removechannel <channel-url>`",
            inline=False
        )

        await context.send(embed=embed)

    @commands.command()
    async def clear(self, context, amount):
        """
        This allows the invoker to delete any given number of messages 
        from the channel it was invoked in
        """

        # Notify the user(s) about the purge
        await context.send(f"Clearing message(s)...")

        # Give them a small timeframe to know
        await sleep(0.75)

        # Increase the amount by 2; because of the message sent by the
        # invoker and the message we just sent
        amount = int(amount) + 2

        deleted_amount = await context.channel.purge(limit=amount)

        # Let the user(s) know that the purge has happened, then
        # delete the information after a small timeframe
        await context.send(f"Cleared {len(deleted_amount)} message(s).",
                           delete_after=1.0)

    # RSS commands:
    @commands.command()
    async def addrss(self, context, url):
        rss_class = RSS(bot=None)
        result = await rss_class.add_feed(url)

        if result == False:
            await context.send(f"The URL already exists in the watchlist database, as a result it was not added.")

        elif result == True:
            await context.send(f"Added the URL to the watchlist database.")

    @commands.command()
    async def removerss(self, context, url):
        rss_class = RSS(bot=None)
        result = await rss_class.remove_feed(url)

        if result == False:
            await context.send(f"The URL doesn't exist in the watchlist database, as a result it was not removed.")

        elif result == True:
            await context.send(f"Removed the URL from the watchlist database.")

    # Google Alerts commands:
    @commands.command()
    async def addalert(self, context, url):
        alert_class = Google_Alerts(bot=None)
        result, keyword = await alert_class.add_alert(url)

        if result == False:
            await context.send(f"The alert for `{keyword}` already exists in the watchlist database, as a result it was not added.")

        elif result == True:
            await context.send(f"Added the alert for `{keyword}` to the watchlist database.")

    @commands.command()
    async def removealert(self, context, url):
        alert_class = Google_Alerts(bot=None)
        result, keyword = await alert_class.remove_alert(url)

        if result == False:
            await context.send(f"The alert for `{keyword}` doesn't exist in the watchlist database, as a result it was not removed.")

        elif result == True:
            await context.send(f"Removed the alert for `{keyword}` from the watchlist database.")

    # Reddit commands:
    @commands.command()
    async def addsubreddit(self, context, subreddit):
        reddit_class = Reddit(bot=None)
        result = await reddit_class.add_subreddit(subreddit.lower())

        if result == False:
            await context.send(f"`/r/{subreddit.lower()}` already exists in the watchlist database, as a result it was not added.")

        elif result == True:
            await context.send(f"Added `/r/{subreddit.lower()}` to the watchlist database.")

    @commands.command()
    async def removesubreddit(self, context, subreddit):
        reddit_class = Reddit(bot=None)
        result = await reddit_class.remove_subreddit(subreddit.lower())

        if result == False:
            await context.send(f"`/r/{subreddit.lower()}` doesn't exist in the watchlist database, as a result it was not removed.")

        elif result == True:
            await context.send(f"Removed `/r/{subreddit.lower()}` from the watchlist database.")

    # Telegram commands:
    @commands.command()
    async def addtelegram(self, context, url):
        telegram_class = Telegram(bot=None)
        result, channel = await telegram_class.add_channel(url)

        if result == False:
            await context.send(f"`{channel}` already exists in the watchlist database, as a result it was not added.")

        elif result == True:
            await context.send(f"Added `{channel}` to the watchlist database.")

    @commands.command()
    async def removetelegram(self, context, url):
        telegram_class = Telegram(bot=None)
        result, channel = await telegram_class.remove_channel(url)

        if result == False:
            await context.send(f"`{channel}` doesn't exist in the watchlist database, as a result it was not removed.")

        elif result == True:
            await context.send(f"Removed `{channel}` from the watchlist database.")

    # Twitter commands:
    @commands.command()
    async def addtweeter(self, context, username):
        twitter_class = Twitter(bot=None)
        result = await twitter_class.add_user(username.lower())

        if result == False:
            await context.send(f"`@{username.lower()}` already exists in the watchlist database, as a result it was not added.")

        elif result == True:
            await context.send(f"Added `@{username.lower()}` to the watchlist database.")

    @commands.command()
    async def removetweeter(self, context, username):
        twitter_class = Twitter(bot=None)
        result = await twitter_class.remove_user(username.lower())

        if result == False:
            await context.send(f"`@{username.lower()}` doesn't exist in the watchlist database, as a result it was not removed.")

        elif result == True:
            await context.send(f"Removed `@{username.lower()}` from the watchlist database.")

    @commands.command()
    async def enablerts(self, context, username):
        twitter_class = Twitter(bot=None)
        result = await twitter_class.enable_retweets(username.lower())

        if result == "0":
            await context.send(f"`@{username.lower()}` doesn't exists in the watchlist database, as a result it was not updated.")

        elif result == "1":
            await context.send(f"Retweets from `@{username.lower()}` will now be displayed.")

        elif result == "2":
            await context.send(f"You've already enabled retweets for `@{username.lower()}`. As a result, the value was not updated.")

    @commands.command()
    async def disablerts(self, context, username):
        twitter_class = Twitter(bot=None)
        result = await twitter_class.disable_retweets(username.lower())

        if result == "0":
            await context.send(f"`@{username.lower()}` doesn't exists in the watchlist database, as a result it was not updated.")

        elif result == "1":
            await context.send(f"You've already disabled retweets for `@{username.lower()}`. As a result, the value was not updated.")

        elif result == "2":
            await context.send(f"Retweets from `@{username.lower()}` will now not be displayed.")

    # YouTube commands:
    @commands.command()
    async def addchannel(self, context, url):
        youtube_class = YouTube(bot=None)
        result, channel_name = await youtube_class.add_channel(url)

        if result == False:
            await context.send(f"`{channel_name}` already exists in the watchlist database, as a result it was not added.")

        elif result == True:
            await context.send(f"Added `{channel_name}` to the watchlist database.")

    @commands.command()
    async def removechannel(self, context, url):
        youtube_class = YouTube(bot=None)
        result, channel_name = await youtube_class.remove_channel(url)

        if result == False:
            await context.send(f"`{channel_name}` doesn't exist in the watchlist database, as a result it was not removed.")

        elif result == True:
            await context.send(f"Removed `{channel_name}` from the watchlist database.")

    @commands.command()
    async def shutdown(self, context):
        await context.send("Shutting down Pwn The Jewels in 3 seconds...")
        await sleep(3)
        await self.bot.close()

def setup(bot):
    bot.add_cog(Commands(bot))
