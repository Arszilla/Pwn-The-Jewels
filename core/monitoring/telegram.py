from datetime import datetime

import aiosqlite
import discord
import feedparser
from core import constants
from discord.ext.tasks import loop


class Telegram():
    def __init__(self, bot):
        self.bot = bot

    async def add_channel(self, url):
        async with aiosqlite.connect(constants.Database.name) as database:
            # Get the Telegram feed's channel name:
            feed = feedparser.parse(url)
            channel = feed.feed.title.split(' – Telegram')[0]

            # Check if the URL exists in the database.
            async with database.execute("SELECT url FROM telegram_rss_links WHERE url=?",
                                        (url,)) as cursor:
                result = await cursor.fetchall()

                # If the URL does NOT exist in the database:
                if len(result) == 0:

                    await database.execute("INSERT INTO telegram_rss_links VALUES (?, ?)",
                                           (url, channel))
                    await database.commit()

                    return True, channel

                # If the URL exists in the database:
                else:
                    return False, channel

    async def remove_channel(self, url):
        async with aiosqlite.connect(constants.Database.name) as database:
            # Get the Telegram feed's channel name:
            feed = feedparser.parse(url)
            channel = feed.feed.title.split(' – Telegram')[0]

            # Check if the URL exists in the database.
            async with database.execute("SELECT url FROM telegram_rss_links WHERE url=?",
                                        (url,)) as cursor:
                result = await cursor.fetchall()

            # If the URL does NOT exist in the database:
            if len(result) == 0:
                return False, channel

            # If the URL exists in the database:
            else:
                await database.execute("DELETE FROM telegram_rss_links WHERE url=?",
                                       (url,))
                await database.commit()

                return True, channel

    # Run this every 30 seconds
    @loop(seconds=30)
    async def monitor_channels(self):
        # Define the channel that'll be used to send the embeds:
        channel = self.bot.get_channel(constants.Channels.telegram_rss)

        async with aiosqlite.connect(constants.Database.name) as database:
            async with database.execute("SELECT * FROM telegram_rss_links") as rss_cursor:
                telegram_channels = await rss_cursor.fetchall()

            for url, telegram_channel in telegram_channels:
                # Get the RSS feed of the URL
                feed = feedparser.parse(url)

                # Get the first entry in the feed
                entry = feed.entries[0]

                async with database.execute("SELECT id FROM telegram_rss_posts WHERE id=?",
                                            (entry.id,)) as id_cursor:
                    result = await id_cursor.fetchall()

                # If the ID does NOT exist in the database:
                if len(result) == 0:
                    # Remove the any links in the title,
                    # as they can ruin the title and the URL embeds:
                    parsed_title = entry.title.split("https://")[0]

                    # If title parsing was unsuccessful:
                    await database.execute("INSERT INTO telegram_rss_posts VALUES (?, ?, ?, ?)",
                                           (entry.id,
                                            telegram_channel,
                                            parsed_title,
                                            entry.link))

                    await database.commit()

                    # Embed the entry
                    embed = discord.Embed(
                        title=parsed_title,
                        url=entry.link,
                        description=f"A new Telegram message in {telegram_channel} has been detected",
                        type="rich",
                        color=0x0088CC
                    )

                    # Embed the author of the post.
                    embed.set_author(
                        name=entry.author,
                    )

                    # Embed the footer
                    embed.set_footer(
                        text="Pwn The Jewels"
                    )

                    # Embed the time
                    embed.timestamp = datetime.utcnow()

                    # Send the Discord embed to the telegram_rss channel.
                    await channel.send(embed=embed)

                # If the ID exists in the database, move on to the next feed.
                else:
                    continue
