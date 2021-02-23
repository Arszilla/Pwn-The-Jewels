from datetime import datetime

import aiosqlite
import asyncpraw
import discord
from core import constants
from discord.ext.tasks import loop


class Reddit():
    def __init__(self, bot):
        self.bot = bot

    async def add_subreddit(self, subreddit):
        async with aiosqlite.connect(constants.Database.name) as database:
            # Check if the subreddit exists in the database.
            async with database.execute("SELECT subreddit FROM reddit_subreddits WHERE subreddit=?",
                                        (subreddit,)) as cursor:
                result = await cursor.fetchall()

                # If the subreddit does NOT exist in the database:
                if len(result) == 0:
                    await database.execute("INSERT INTO reddit_subreddits(subreddit) VALUES (?)",
                                           (subreddit,))
                    await database.commit()

                    return True

                # If the subreddit exists in the database:
                else:
                    return False

    async def remove_subreddit(self, subreddit):
        async with aiosqlite.connect(constants.Database.name) as database:
            # Check if the subreddit exists in the database.
            async with database.execute("SELECT subreddit FROM reddit_subreddits WHERE subreddit=?",
                                        (subreddit,)) as cursor:
                result = await cursor.fetchall()

            # If the subreddit does NOT exist in the database:
            if len(result) == 0:
                return False

            # If the subreddit exists in the database:
            else:
                await database.execute("DELETE FROM reddit_subreddits WHERE subreddit=?",
                                       (subreddit,))
                await database.commit()

                return True

    # Run this every 30 seconds
    @loop(seconds=30)
    async def monitor_subreddit(self):
        # Define the channel that'll be used to send the embeds:
        channel = self.bot.get_channel(constants.Channels.reddit_rss)

        async with aiosqlite.connect(constants.Database.name) as database:
            # Turn the necessary values into a dictionary,
            # in order to unpack them in the next step.
            config = {"client_id": constants.Reddit.client_id,
                      "client_secret": constants.Reddit.secret,
                      "user_agent": constants.Reddit.user_agent}

            # Initiate asyncpraw by unpacking the config dictionary.
            async with asyncpraw.Reddit(**config) as reddit:
                # Get all the subreddits in the database:
                async with database.execute("SELECT * FROM reddit_subreddits") as sub_cursor:
                    subreddit_list = await sub_cursor.fetchall()

                for sub in [subreddit[0] for subreddit in subreddit_list]:
                    subreddit = await reddit.subreddit(sub)

                    # Gather the submissions in the subreddit, with a limit of 1 submission.
                    async for submission in subreddit.new(limit=1):
                        # Check if the post has been saved in the database:
                        async with database.execute("SELECT id FROM reddit_posts WHERE id=?",
                                                    (str(submission),)) as id_cursor:
                            result = await id_cursor.fetchall()

                        # If the post does NOT exist in the database:
                        if len(result) == 0:
                            await database.execute("INSERT INTO reddit_posts VALUES (?, ?, ?, ?, ?)",
                                                    (str(submission),
                                                    sub,
                                                    str(submission.author),
                                                    submission.title,
                                                    f"https://reddit.com{submission.permalink}"))
                            await database.commit()

                            # 'submission.shortlink' is an alternative to 'submission.permalink',
                            # but in order to use it, 'https://reddit.com' has to be removed.
                            embed = discord.Embed(
                                title=submission.title,
                                url=f"https://reddit.com{submission.permalink}",
                                type="rich",
                                description=f"A new post in /r/{sub} by /u/{submission.author}\n",
                                color=0xFF4500
                            )

                            # Get the profile picture of the author:
                            redditor = await reddit.redditor(str(submission.author))
                            await redditor.load()
                            profile_picture = redditor.icon_img

                            # Embed the author of the post.
                            embed.set_author(
                                name=f"/u/{submission.author.name}",
                                url=f"https://reddit.com/u/{submission.author}",
                                icon_url=profile_picture
                            )

                            # Embed the footer
                            embed.set_footer(
                                text="Pwn The Jewels"
                            )

                            # Embed the time
                            embed.timestamp = datetime.utcnow()

                            # Send the Discord embed to the Reddit channel.
                            await channel.send(embed=embed)

                        # If the post exists in the database, move on to the next subreddit.
                        else:
                            continue
