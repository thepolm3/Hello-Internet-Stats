"""Gets the hello internet rss feed"""
import requests

RSS_FEED = "http://www.hellointernet.fm/podcast?format=rss"
RSS_FILE_NAME = "rss-feed.xml"

def main():
    req = requests.get(RSS_FEED)
    with open(RSS_FILE_NAME, 'wb+') as rss_file:
        rss_file.write(req.content)

if __name__ == '__main__':
    main()
