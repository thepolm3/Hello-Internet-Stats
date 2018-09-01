# Hello Internet Stats
Apologies for the incredibly messy repository, maybe one day I'll clean it up and make things more general, for now this was a bit of a bodge job

# Requirements
* [Python 3.7+](https://python.org)
* To fetch reddit thread you need a [Client id and secret in secret.py](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example)
* See requirements.txt for required packages

Currently episodes 11-108 are already in the rss feed so you need only run graph.py with any modifications to generate a graph with matplotlib

For a list of episode attributes see get_episodes.py

To regenerate the episode list run build_episode_list.py
To only regenerate the rss feed, episode list or reddit threads run those files individually