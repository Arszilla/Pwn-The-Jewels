from datetime import datetime
from re import search, split

import aiosqlite
import discord
from core import constants
from discord.ext.tasks import loop
from googleapiclient.discovery import build


class YouTube():
    def __init__(self, bot):
        self.bot = bot

        self.youtube = build(
            "youtube",
            "v3",
            developerKey=constants.Youtube.api_key
        )

        self.https_options = [
            "https://www.youtube.com/channel/",
            "https://www.youtube.com/user/",
            "https://youtube.com/channel/",
            "https://youtube.com/user/"
        ]

    async def add_channel(self, url):
        # Use the given possibilities for the Youtube URL to grab the channel name/ID
        for option in self.https_options:
            if search(option, url):
                channel_name = split(option, url)[1]

                # If the URL followed "/user/channel_name" format,
                # get the channel's ID
                if "user" in option:
                    channel_id_request = self.youtube.channels().list(
                        part="id",
                        forUsername=channel_name
                    )

                    channel_id_response = channel_id_request.execute()
                    channel_id = channel_id_response["items"][0]["id"]

                # If the URL followed "/channel/channel_id" format,
                # save it as channel_id
                else:
                    channel_id = channel_name

        async with aiosqlite.connect(constants.Database.name) as database:
            # Check if the channel_id exists in the database.
            async with database.execute("SELECT channel_id FROM youtube_channels WHERE channel_id=?",
                                        (channel_id,)) as cursor:
                result = await cursor.fetchall()

                # If the channel_id exists in the database:
                if len(result) == 0:
                    # Get the channel's display name:
                    channel_name_request = self.youtube.channels().list(
                        part="snippet",
                        id=channel_id
                    )

                    channel_name_response = channel_name_request.execute()
                    channel_name = channel_name_response["items"][0]["snippet"]["title"]

                    await database.execute("INSERT INTO youtube_channels VALUES (?, ?)",
                                           (channel_id, channel_name))
                    await database.commit()

                    return True, channel_name

                # If the channel_id does NOT exists in the database:
                else:
                    return False

    async def remove_channel(self, url):
        # Use the given possibilities for the Youtube URL to grab the channel name/ID
        for option in self.https_options:
            if search(option, url):
                channel_name = split(option, url)[1]

                # If the URL followed "/user/channel_name" format,
                # get the channel's ID
                if "user" in option:
                    request = self.youtube.channels().list(
                        part="id",
                        forUsername=channel_name
                    )

                    response = request.execute()
                    channel_id = response["items"][0]["id"]

                # If the URL followed "/channel/channel_id" format,
                # save it as channel_id
                else:
                    channel_id = channel_name

        async with aiosqlite.connect(constants.Database.name) as database:
            # Check if the channel_id exists in the database.
            async with database.execute("SELECT channel_id FROM youtube_channels WHERE channel_id=?",
                                        (channel_id,)) as cursor:
                result = await cursor.fetchall()

                # If the URL does NOT exist in the database:
                if len(result) == 0:
                    return False

                # If the URL exists in the database:
                else:
                    async with database.execute("SELECT channel_name FROM youtube_channels WHERE channel_id=?",
                                                (channel_id,)) as channel_name_cursor:
                        result = await channel_name_cursor.fetchall()

                    channel_name = [channel_name[0] for channel_name in result][0]

                    await database.execute("DELETE FROM youtube_channels WHERE channel_id=?",
                                           (channel_id,))
                    await database.commit()

                    return True, channel_name

    # Run this every 30 seconds
    @loop(seconds=30)
    async def monitor_videos(self):
        async with aiosqlite.connect(constants.Database.name) as database:
            # Define the channel that'll be used to send the embeds:
            channel = self.bot.get_channel(constants.Channels.youtube_rss)

            async with database.execute("SELECT * FROM youtube_channels") as channel_cursor:
                channel_results = await channel_cursor.fetchall()

            for channel_id, channel_name in channel_results:
                video_id_request = self.youtube.activities().list(
                    part="contentDetails",
                    channelId=channel_id
                )

                video_id_response = video_id_request.execute()
                video_id = video_id_response["items"][0]["contentDetails"]["upload"]["videoId"]

                # Check if the given video ID exists in the database:
                async with database.execute("SELECT video_id FROM youtube_videos WHERE video_id=?",
                                            (video_id,)) as video_id_cursor:
                    result = await video_id_cursor.fetchall()

                # If the video does NOT exist in the database:
                if len(result) == 0:
                    # Get the video's details:
                    video_info_request = self.youtube.videos().list(
                        part="snippet",
                        id=video_id
                    )

                    video_info_response = video_info_request.execute()

                    # Get the video's name:
                    video_name = video_info_response["items"][0]["snippet"]["title"]

                    # Get the video's description:
                    # video_description = video_info_response["items"][0]["snippet"]["description"]

                    await database.execute("INSERT INTO youtube_videos VALUES (?, ?, ?, ?, ?)",
                                            (channel_id,
                                            channel_name,
                                            video_id,
                                            video_name,
                                            f"https://www.youtube.com/watch?v={video_id}"))
                    await database.commit()

                    embed = discord.Embed(
                        title=video_name,
                        url=f"https://www.youtube.com/watch?v={video_id}",
                        type="rich",
                        description=f"{channel_name} just uploaded a new video on YouTube",
                        color=0xFF0000
                    )

                    channel_avatar_request = self.youtube.channels().list(
                        part="snippet",
                        id=channel_id
                    )

                    channel_avatar_response = channel_avatar_request.execute()

                    # Embed the channel name.
                    embed.set_author(
                        name=channel_name,
                        url=f"https://youtube.com/channel/{channel_id}",
                        icon_url=channel_avatar_response["items"][0]["snippet"]["thumbnails"]["high"]["url"]
                    )

                    # Embed the footer
                    embed.set_footer(
                        text="Pwn The Jewels",
                        icon_url=constants.Bot.profile_picture
                    )

                    # Embed the time
                    embed.timestamp = datetime.utcnow()

                    await channel.send(embed=embed)

                # If the video exists in the database:
                else:
                    continue
