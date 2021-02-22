from datetime import datetime
from re import compile, sub

import aiosqlite
import discord
import feedparser
from discord.ext.tasks import loop

from core import constants


class Google_Alerts():
    def __init__(self, bot):
        self.bot = bot

    async def add_alert(self, url):
        async with aiosqlite.connect(constants.Database.name) as database:
            # Get the alert's keyword:
            feed = feedparser.parse(url)
            keyword = feed.feed.title.split('"')[1].split('"')[0]

            
            # Check if the URL exists in the database.
            async with database.execute("SELECT url FROM google_alerts_links WHERE url=?",
                                        (url,)) as cursor:
                result = await cursor.fetchall()

                # If the URL does NOT exist in the database:
                if len(result) == 0:
                    await database.execute("INSERT INTO google_alerts_links VALUES (?, ?)",
                                           (url, keyword))
                    await database.commit()

                    return True, keyword

                # If the URL exists in the database:
                else:
                    return False, keyword

    async def remove_alert(self, url):
        async with aiosqlite.connect(constants.Database.name) as database:
            # Get the alert's keyword:
            feed = feedparser.parse(url)
            keyword = feed.feed.title.split('"')[1].split('"')[0]

            # Check if the URL exists in the database.
            async with database.execute("SELECT url FROM google_alerts_links WHERE url=?",
                                        (url,)) as cursor:
                result = await cursor.fetchall()

            # If the URL does NOT exist in the database:
            if len(result) == 0:
                return False, keyword

            # If the URL exists in the database:
            else:
                await database.execute("DELETE FROM google_alerts_links WHERE url=?",
                                       (url,))
                await database.commit()

                return True, keyword

    # Run this every 30 seconds
    @loop(seconds=30)
    async def monitor_alerts(self):
        # Define the channel that'll be used to send the embeds:
        channel = self.bot.get_channel(constants.Channels.google_rss)

        async with aiosqlite.connect(constants.Database.name) as database:
            async with database.execute("SELECT * FROM google_alerts_links") as rss_cursor:
                rss_links = await rss_cursor.fetchall()

            for url, keyword in rss_links:
                # Get the RSS feed of the URL
                feed = feedparser.parse(url)

                # Get the first entry in the feed
                entry = feed.entries[0]

                # Parse the entry ID and remove "tag:google.com,2013:googlealerts/feed:" etc.
                entry_id = entry.id.split("/feed:")[1]

                async with database.execute("SELECT id FROM google_alerts_posts WHERE id=?",
                                            (entry_id,)) as id_cursor:
                    result = await id_cursor.fetchall()

                # If the ID does NOT exist in the database:
                if len(result) == 0:
                    # Try to remove the "<b> </b>" tags from the entry title if they exist:
                    tags = compile(r"<[^>]+>")
                    parsed_title = sub(tags, "", entry.title)

                    # Parse the entry link so ther's no "https://www.google.com/" and "&ct=ga" etc.
                    link = entry.link
                    link = link.split("&url=")[1].split("&ct=")[0]

                    await database.execute("INSERT INTO google_alerts_posts VALUES (?, ?, ?, ?)",
                                            (entry_id,
                                            keyword,
                                            parsed_title,
                                            link))

                    await database.commit()

                    # Embed the entry
                    embed = discord.Embed(
                        title=parsed_title,
                        url=link,
                        description=f"A new Google Alert for the keyword {keyword} has been detected",
                        type="rich",
                        color=0xF4B400
                    )

                    # Embed the author of the post.
                    embed.set_author(
                        name="Google Alerts",
                        url="https://www.google.com/alerts"
                    )

                    # Embed the footer
                    embed.set_footer(
                        text="Pwn The Jewels"
                    )

                    # Embed the time
                    embed.timestamp = datetime.utcnow()

                    # Send the Discord embed to the google_rss channel.
                    await channel.send(embed=embed)

                # If the ID exists in the database, move on to the next feed.
                else:
                    continue
