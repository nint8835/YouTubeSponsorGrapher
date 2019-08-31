import os
import json
import re

from dotenv import load_dotenv
from googleapiclient.discovery import build

blacklisted_sponsors = {"patreon", "bit.ly"}

load_dotenv()

client = build("youtube", "v3", developerKey=os.environ["YOUTUBE_API_KEY"])

with open("channels.json") as f:
    channels = json.load(f)

sponsors = {}

for channel in channels:
    sponsors[channel["display_name"]] = []
    channel_videos = []
    results = (
        client.search()
        .list(channelId=channel["id"], part="snippet", order="date", maxResults=50)
        .execute()
    )
    channel_videos += results["items"]
    while "nextPageToken" in results:
        results = (
            client.search()
            .list(
                channelId=channel["id"],
                part="snippet",
                order="date",
                maxResults=50,
                pageToken=results["nextPageToken"],
            )
            .execute()
        )
        channel_videos += results["items"]

    for video in channel_videos:
        for regex in channel["sponsor_regexes"]:
            print(video["snippet"]["description"])
            sponsor = re.findall(regex, video["snippet"]["description"])
            if sponsor:
                sponsor = sponsor[0].lower().replace("www.", "")
            if (
                sponsor
                and sponsor not in sponsors[channel["display_name"]]
                and not any(
                    sponsor in blacklisted_sponsor
                    for blacklisted_sponsor in blacklisted_sponsors
                )
            ):
                sponsors[channel["display_name"]].append(sponsor)

with open("sponsors.json", "w") as f:
    json.dump(sponsors, f)
