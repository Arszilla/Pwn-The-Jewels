import aiosqlite
import asyncpraw
import discord
from discord.ext.tasks import loop

from core import constants


class Reddit():
    def __init__(self, bot):
        self.bot = bot

    async def add_subreddit(self, subreddit):
        connection = None

        try:
            connection = await aiosqlite.connect(constants.Database.name)
            cursor = await connection.cursor()

            await cursor.execute("SELECT subreddit FROM reddit_subreddits WHERE subreddit=?",
                                 (subreddit,))
            result = await cursor.fetchall()

            if len(result) == 0:
                await cursor.execute("INSERT INTO reddit_subreddits(subreddit) VALUES (?)",
                                     (subreddit,))
                await connection.commit()

                return True

            else:
                return False

        except aiosqlite.Error as error:
            print(error)

        finally:
            if connection:
                await connection.close()

    async def remove_subreddit(self, subreddit):
        connection = None

        try:
            connection = await aiosqlite.connect(constants.Database.name)
            cursor = await connection.cursor()

            await cursor.execute("SELECT subreddit FROM reddit_subreddits WHERE subreddit=?",
                                 (subreddit,))
            result = await cursor.fetchall()

            if len(result) == 0:
                return False

            else:
                await cursor.execute("DELETE FROM reddit_subreddits WHERE subreddit=?",
                                     (subreddit,))
                await connection.commit()

                return True

        except aiosqlite.Error as error:
            print(error)

        finally:
            if connection:
                await connection.close()

    # Run this every 30 seconds
    @loop(seconds=30)
    async def monitor_subreddit(self):
        connection = None

        try:
            # Initate connection to the database
            connection = await aiosqlite.connect(constants.Database.name)
            cursor = await connection.cursor()

            # Turn the necessary values into a dictionary,
            # in order to unpack them in the next step
            config = {"client_id": constants.Reddit.client_id,
                      "client_secret": constants.Reddit.secret,
                      "user_agent": constants.Reddit.user_agent}

            # Initiate asyncpraw by unpacking the config dictionary
            async with asyncpraw.Reddit(**config) as reddit:
                # Define the channel:
                await self.bot.wait_until_ready()
                channel = self.bot.get_channel(constants.Channels.reddit_rss)

                # Get all the subreddits in the database:
                await cursor.execute("SELECT * FROM reddit_subreddits")
                subreddit_list = await cursor.fetchall()

                # Turn the list of tuples into a list:
                subreddit_list = [item for sub in subreddit_list for item in sub]

                for sub in subreddit_list:
                    subreddit = await reddit.subreddit(sub)

                    async for submission in subreddit.new(limit=1):
                        await cursor.execute("SELECT id FROM reddit_posts WHERE id=?",
                                             (str(submission),))
                        result = await cursor.fetchall()

                        if len(result) == 0:
                            await cursor.execute("INSERT INTO reddit_posts VALUES (?, ?, ?, ?, ?)",
                                                 (str(submission),
                                                  str(sub),
                                                  str(submission.author.name),
                                                  str(submission.title),
                                                  f"https://reddit.com{str(submission.permalink)}"))
                            await connection.commit()

                            # 'submission.shortlink' is an alternative to 'submission.permalink',
                            # but in order to use it, 'https://reddit.com' has to be removed.
                            embed = discord.Embed(
                                title=submission.title,
                                url=f"https://reddit.com{submission.permalink}",
                                type="rich",
                                description=f"A new post in /r/{sub} by /u/{submission.author.name}\n",
                                color=0xFF4500
                            )

                            # Embed the author of the post.
                            embed.set_author(
                                name=f"/u/{submission.author.name}",
                                url=f"https://reddit.com/u/{submission.author.name}"
                            )

                            # Send the Discord embed to the Reddit channel.
                            await channel.send(embed=embed)

                        # If the post already exists in the database, move on to the next subreddit.
                        else:
                            continue

        except aiosqlite.Error as error:
            print(error)

        finally:
            if connection:
                await connection.close()
