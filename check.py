import requests
import os.path
from mastodon import Mastodon
import feedparser
NewsFeed = feedparser.parse("https://astro.theoj.org/feed")
with open("mastodonkeys.txt") as f:
    lines = f.readlines()
    MASTODON_ACCESS_TOKEN, = [l.strip() for l in lines]

mastodon = Mastodon(
        access_token = MASTODON_ACCESS_TOKEN,
        api_base_url = "https://botsin.space/",
        )


oldcf = "oldcitations.txt"
firstrun = not os.path.isfile(oldcf)
if not firstrun:
    with open(oldcf,"r") as f:
        oldc = f.readlines()
else:
    oldc = []
oldc = [l.strip() for l in oldc]

debug = False # "2020arXiv201006614G"

for entry in NewsFeed.entries:
    if "doi" in entry["id"]:
        bibcode = entry["id"]
        if bibcode not in oldc or bibcode == debug:
            if not firstrun:
                url = entry["id"]
                title = entry["title"]
                summary = entry["summary"]

                maxlength = 500 - len(url) - 10
                text = title + "\n\n" + summary
                if len(text)>maxlength:
                    text = text[:maxlength-2] + '..' 
                text += "\n"+ url
                
                try:
                    url = entry["media_content"][0]["url"]
                    mime_type = entry["media_content"][0]["type"]

                    res = requests.get(url, stream = True)
                    if res.status_code == 200:
                        mp = mastodon.media_post(res.raw,mime_type=mime_type)
                        media_ids = [mp["id"]]
                except:
                    media_ids = None
                mastodon.status_post(text, media_ids=media_ids)
            if bibcode not in oldc:
                with open(oldcf,"a") as f:
                    print(bibcode,file=f)
                break



