"""Adds reddit thread to each episode"""

import pickle
from pprint import pprint
import praw
from prawcore.exceptions import ServerError
from secret import client_id, client_secret

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent='Python:helloInternetStats:v1 (by /u/thepolm3)')

#reddit search doesn't support unicode, so this exception must be made
MANUAL_UPDATES = [{"number":101, "reddit-thread":reddit.submission('8f4acy')}]

def episodes_with_thread(episodes, reddit):

    for episode in episodes:
        search_results = reddit.subreddit('CGPGrey').search(episode['title'])
        try:
            episode_discussion = next(search_results, None)
        except ServerError:
            continue

        episode['reddit-thread'] = episode_discussion
        if episode_discussion is not None:
            print(episode['title'])

    for update in MANUAL_UPDATES:
        for episode in episodes:
            if episode['number'] == update['number']:
                episode.update(update)
                print(f"Updating episode {episode['number']} manually")
                pprint(episode)
                break

    return episodes


if __name__ == '__main__':
    with open('episodes.pickle', 'rb') as f:
        episodes = pickle.load(f)

    episodes = episodes_with_thread(episodes, reddit)

    with open('episodes.pickle', 'wb') as f:
        pickle.dump(episodes, f, pickle.HIGHEST_PROTOCOL)
