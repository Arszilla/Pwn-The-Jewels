from datetime import datetime
from re import sub

import aiosqlite
import discord
import tweepy
from discord.ext.tasks import loop

from core import constants


class Twitter():
    def __init__(self, bot):
        self.bot = bot

    async def add_user(self, username):
        async with aiosqlite.connect(constants.Database.name) as database:
            # Check if the username exists in the database.
            async with database.execute("SELECT username FROM twitter_usernames WHERE username=?",
                                        (username,)) as cursor:
                result = await cursor.fetchall()

                # If the username does NOT exist in the database:
                if len(result) == 0:
                    await database.execute("INSERT INTO twitter_usernames VALUES (?, ?)",
                                           (username, False))
                    await database.commit()

                    return True

                # If the username exists in the database:
                else:
                    return False

    async def remove_user(self, username):
        async with aiosqlite.connect(constants.Database.name) as database:
            # Check if the username exists in the database.
            async with database.execute("SELECT username FROM twitter_usernames WHERE username=?",
                                        (username,)) as cursor:
                result = await cursor.fetchall()

            # If the username does NOT exist in the database:
            if len(result) == 0:
                return False

            # If the username exists in the database:
            else:
                await database.execute("DELETE FROM twitter_usernames WHERE username=?",
                                       (username,))
                await database.commit()

                return True

    async def enable_retweets(self, username):
        async with aiosqlite.connect(constants.Database.name) as database:
            # Check if the username exists in the database.
            async with database.execute("SELECT username FROM twitter_usernames WHERE username=?",
                                        (username,)) as username_cursor:
                result = await username_cursor.fetchall()

                # If the username does NOT exist in the database:
                if len(result) == 0:
                    return "0"

                # If the username exists in the database:
                else:
                    # Check if it the value is already set to 'True'
                    async with database.execute("SELECT retweets FROM twitter_usernames WHERE username=?",
                                                (username,)) as boolean_cursor:
                        result = await boolean_cursor.fetchall()

                        # Grab the value for the result
                        result = [username[0] for username in result][0]

                        # If the value is NOT set to "True":
                        if result == 0:
                            await database.execute("UPDATE twitter_usernames SET retweets=? WHERE username=?",
                                                   (True, username))
                            await database.commit()

                            return "1"

                        # If the value is already set to "TRUE":
                        else:
                            return "2"

    async def disable_retweets(self, username):
        async with aiosqlite.connect(constants.Database.name) as database:
            # Check if the username exists in the database.
            async with database.execute("SELECT username FROM twitter_usernames WHERE username=?",
                                        (username,)) as username_cursor:
                result = await username_cursor.fetchall()

                # If the username does NOT exist in the database:
                if len(result) == 0:
                    return "0"

                # If the username exists in the database:
                else:
                    # Check if it the value is already set to 'True'
                    async with database.execute("SELECT retweets FROM twitter_usernames WHERE username=?",
                                                (username,)) as boolean_cursor:
                        result = await boolean_cursor.fetchall()

                        # Grab the value for the result
                        result = [username[0] for username in result][0]

                        # If the value is already set to "False":
                        if result == 0:
                            return "1"

                        # If the value is NOT set to "False":
                        else:
                            await database.execute("UPDATE twitter_usernames SET retweets=? WHERE username=?",
                                                   (False, username))
                            await database.commit()

                            return "2"

    # Run this every 30 seconds
    @loop(seconds=30)
    async def monitor_tweets(self):
        # Setup tweepy:
        authentication = tweepy.OAuthHandler(constants.Twitter.consumer_key,
                                             constants.Twitter.consumer_secret)

        authentication.set_access_token(constants.Twitter.access_token,
                                        constants.Twitter.access_token_secret)

        twitter_api = tweepy.API(authentication)

        # Define the channel that'll be used to send the embeds:
        channel = self.bot.get_channel(constants.Channels.twitter_rss)

        async with aiosqlite.connect(constants.Database.name) as database:
            async with database.execute("SELECT * FROM twitter_usernames") as twitter_cursor:
                twitter_list = await twitter_cursor.fetchall()

            for username, rt_status in twitter_list:
                # If retweets are disabled:
                if rt_status == 0:
                    user_feed = twitter_api.user_timeline(screen_name=username,
                                                          include_rts=False,
                                                          exclude_replies=True,
                                                          tweet_mode="extended",
                                                          count=1)

                # If retweets are enabled:
                elif rt_status == 1:
                    user_feed = twitter_api.user_timeline(screen_name=username,
                                                          include_rts=True,
                                                          exclude_replies=False,
                                                          tweet_mode="extended",
                                                          count=1)

                tweet = user_feed[0]

                # Check if the given tweet exists in the database:
                async with database.execute("SELECT id FROM twitter_tweets WHERE id=?",
                                            (tweet.id,)) as id_cursor:
                    result = await id_cursor.fetchall()

                # If the tweet does NOT exist in the database:
                if len(result) == 0:
                    # The line below has been commented out because
                    # stuff like Spotify etc. use "https://t.co/" links.
                    # As a result, this leaves some embeds looking weird.
                    # For now, "https://t.co/" links will stay in embeds,
                    # until a proper solution can be found.

                    # Remove any "https://t.co/" URLs in the tweet:
                    # tweet_text = sub(r"https://t.co/\w+", "", tweet.full_text)

                    await database.execute("INSERT INTO twitter_tweets VALUES (?, ?, ?, ?)",
                                            (tweet.id,
                                            username,
                                            tweet.full_text,
                                            f"https://twitter.com/{username}/status/{tweet.id}"))
                    await database.commit()

                    # Check if the tweet has "RT" at the beginning of the string.
                    # This is done in order to remove the retweet indicator later on.
                    if tweet.full_text.split()[0] == "RT":
                        # Embed the retweet
                        embed = discord.Embed(
                            title=f"{username} just retweeted",
                            url=f"https://twitter.com/{username}/status/{tweet.id}",
                            type="rich",
                            description=tweet.full_text.split(" ", 1)[1],
                            color=0x1DA1F2
                        )

                    else:
                        # Embed the tweet
                        embed = discord.Embed(
                            title=f"{username} just tweeted",
                            url=f"https://twitter.com/{username}/status/{tweet.id}",
                            type="rich",
                            description=tweet.full_text,
                            color=0x1DA1F2
                        )

                    # Embed the author of the post.
                    embed.set_author(
                        name=f"@{username}",
                        url=f"https://twitter.com/{username}",
                        icon_url=tweet.user.profile_image_url
                    )

                    # If there are any images in the tweet, grab the first image:
                    if "media" in tweet.entities:
                        embed.set_image(
                            url=tweet.extended_entities["media"][0]["media_url"]
                        )

                    # Embed the footer
                    embed.set_footer(
                        text="Pwn The Jewels"
                    )

                    # Embed the time
                    embed.timestamp = datetime.utcnow()

                    # Send the Discord embed to the Twitter channel.
                    await channel.send(embed=embed)

                # If the tweet exists in the database, move on to the next user.
                else:
                    continue
