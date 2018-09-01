import get_rss_feed
import get_episodes
import get_reddit_thread

print('Downloading rss feed')
get_rss_feed.main()

print('Parsing rss feed and getting episode data')
get_episodes.main()

print('Getting reddit thread')
get_reddit_thread.main()

print('Finished')