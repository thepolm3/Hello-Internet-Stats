"""Gets the episodes from the RSS feed and dumps them to episodes.pickle"""

from xml.etree import ElementTree
from datetime import datetime, timedelta
import pickle
from pprint import pprint
from dateutil.parser import parse as parse_datetime
import requests
from get_rss_feed import RSS_FILE_NAME

#These episodes don't have the standard bitrate as far as I can tell
MANUAL_UPDATES = [{"number":94, "length":timedelta(hours=1, minutes=53, seconds=57)},
                  {"number":103, "length":timedelta(hours=1, minutes=43, seconds=25)}]

def get_episodes(xmlTree):
    """Gets episode data from the xml"""

    episodes = []
    bitrate = 16000
    for item in xmlTree.getroot()[0].findall('item')[::-1]:
        episode = {}
        episodes.append(episode)

        title = item.find('title').text

        episode['date'] = parse_datetime(item.find('pubDate').text)
        episode['mp3'] = item.find('{http://www.rssboard.org/media-rss}content').attrib['url']
        episode['title'] = title
        episode['link'] = item.find('link').text
        duration = item.find('{http://www.itunes.com/dtds/podcast-1.0.dtd}duration')

        #some episodes do not have a defined duration, so we check the actual MP3
        if duration is None:
            print(f"Couldn't get file duration for {episode['title']}")
            print(f"Attempting to get from {episode['mp3']}")

            h = requests.head(episode['mp3'], allow_redirects=True)
            header = h.headers

            size = int(header.get('content-length'))
            length = timedelta(seconds=size//bitrate)
            print(f'final length: {length}')

        else:
            t = datetime.strptime(duration.text, "%H:%M:%S")
            length = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)

        episode['length'] = length
        episode['number'] = -1

        #Curse you Grey and your episode numbering
        #gets the episode number if it can be found in the title
        start_of_number = min([i for i in range(len(title)) if title[i].isdigit()], default=None)
        if start_of_number is None:
            continue

        end_of_number = min([i for i in range(start_of_number, len(title)) if not title[i].isdigit()], default=None)
        if end_of_number is None:
            continue

        episode_number = episode['title'][start_of_number:end_of_number]

        episode['number'] = int(episode_number)


    #interpolates missing numbers (thanks grey)
    numbers = {episode['number'] for episode in episodes}
    for i, episode in enumerate(episodes):
        if episode['number'] != -1:
            continue

        number = episodes[i-1]['number'] + 1
        if number in numbers:
            continue

        episode['number'] = number

    for update in MANUAL_UPDATES:
        for episode in episodes:
            if episode['number'] == update['number']:
                episode.update(update)
                print(f"Updating episode {episode['number']} manually")
                pprint(episode)
                break

    return episodes

if __name__ == '__main__':
    tree = ElementTree.parse(RSS_FILE_NAME)

    episodes = get_episodes(tree)

    with open('episodes.pickle', 'wb') as f:
        pickle.dump(episodes, f, pickle.HIGHEST_PROTOCOL)
