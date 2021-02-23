from datetime import datetime

import aiosqlite
import discord
import feedparser
from core import constants
from discord.ext.tasks import loop


class RSS():
    def __init__(self, bot):
        self.bot = bot

    async def add_feed(self, url):
        async with aiosqlite.connect(constants.Database.name) as database:
            # Check if the URL exists in the database.
            async with database.execute("SELECT url FROM general_rss_links WHERE url=?",
                                        (url,)) as cursor:
                result = await cursor.fetchall()

                # If the URL does NOT exist in the database:
                if len(result) == 0:
                    await database.execute("INSERT INTO general_rss_links(url) VALUES (?)",
                                           (url,))
                    await database.commit()

                    return True

                # If the URL exists in the database:
                else:
                    return False

    async def remove_feed(self, url):
        async with aiosqlite.connect(constants.Database.name) as database:
            # Check if the URL exists in the database.
            async with database.execute("SELECT url FROM general_rss_links WHERE url=?",
                                        (url,)) as cursor:
                result = await cursor.fetchall()

            # If the URL does NOT exist in the database:
            if len(result) == 0:
                return False

            # If the URL exists in the database:
            else:
                await database.execute("DELETE FROM general_rss_links WHERE url=?",
                                       (url,))
                await database.commit()

                return True

    # Run this every 30 seconds
    @loop(seconds=30)
    async def monitor_rss(self):
        # Define the channel that'll be used to send the embeds:
        channel = self.bot.get_channel(constants.Channels.general_rss)

        async with aiosqlite.connect(constants.Database.name) as database:
            async with database.execute("SELECT * FROM general_rss_links") as rss_cursor:
                rss_links = await rss_cursor.fetchall()

            # Turn the list of tuples into a list:
            rss_links = [url[0] for url in rss_links]

            for url in rss_links:
                # Get the RSS feed of the URL
                feed = feedparser.parse(url)

                # Get the first entry in the feed
                entry = feed.entries[0]

                async with database.execute("SELECT id FROM general_rss_posts WHERE id=?",
                                            (str(entry.id),)) as id_cursor:
                    result = await id_cursor.fetchall()

                    # If the ID does NOT exist in the database:
                    if len(result) == 0:
                        await database.execute("INSERT INTO general_rss_posts VALUES (?, ?, ?)",
                                                (str(entry.id),
                                                str(entry.title),
                                                str(entry.link)))
                        await database.commit()

                        # Embed the entry
                        embed = discord.Embed(
                            title=entry.title,
                            url=entry.link,
                            type="rich",
                            color=0x777777
                        )

                        # If the post has an author, try to embed it:
                        try:
                            # Embed the author of the post.
                            embed.set_author(
                                name=entry.author,
                            )

                        # If the post doesn't have an author, embed 'unknown author'
                        except AttributeError:
                            embed.set_author(
                                name="Unknown Author",
                            )

                        # Embed the footer
                        embed.set_footer(
                            text="Pwn The Jewels"
                        )

                        # Embed the time
                        embed.timestamp = datetime.utcnow()

                        # Send the Discord embed to the general_rss channel.
                        await channel.send(embed=embed)

                    # If the ID exists in the database, move on to the next feed.
                    else:
                        continue
