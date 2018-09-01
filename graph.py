"""Graphs the episodes"""

import pickle
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
from matplotlib.dates import date2num
import numpy as np

with open('episodes.pickle', 'rb') as f:
    episodes = pickle.load(f)

#for our purposes we need a reddit thread
for episode in episodes:
    if episode['reddit-thread'] is None:
        print(f"{episode['title']} has no reddit thread")
        episodes.pop(episodes.index(episode))

lengths = [episode['length'].seconds/3600 for episode in episodes]
numbers = [episode['number'] for episode in episodes]
titles = [episode['title'] for episode in episodes]
dates = [episode['date'] for episode in episodes]

no_of_comments = []
for episode in episodes:
    no_of_comments.append(episode['reddit-thread'].num_comments)

days_since = [0]
for i in range(1, len(episodes)):
    days_since.append((episodes[i]['date'] - episodes[i-1]['date']).days)



#available values: lengths, numbers, titles, dates, no_of_comments, days_since
x, y = days_since, no_of_comments
s, c = lengths*50, date2num(dates)
xlabel = "Days since last episode"
ylabel = "Number of reddit comments"
title = "Days since last episode vs Engagement in Hello Internet episodes"

############## bar chart
# top_values = [e['date'] for e in episodes[4::5]]
# top_labels = [str(e['number']) for e in episodes[4::5]]
# fig = plt.figure(figsize=(20,10), dpi=300)
# ax = host_subplot(111, axes_class=AA.Axes)

# ax2 = ax.twin()
# ax2.set_xticks(top_values)
# ax2.set_xticklabels(top_labels, rotation=45)
# ax2.grid(zorder=0)

# ax2.axis["right"].major_ticklabels.set_visible(False)
# ax2.axis["top"].major_ticklabels.set_visible(True)

# ax.bar(x, y, width=3, zorder=3)
# ax.xaxis_date()

# longest_episodes = sorted(episodes, key=lambda ep: ep['length'], reverse=True)[:5]

# for ep in longest_episodes:
#   height = ep['length'].seconds/3600
#   ax.text(ep['date'], height,
#       str(ep['number']),
#       ha = 'center', va='bottom')

#fig.savefig('graph.png')

fig = plt.figure(figsize=(10, 10), dpi=300)
plt.scatter(x, y, s=s, c=c, cmap='plasma', alpha=1)

#set up the colorbar
first_episode_tick = ((numbers[0] + 5)//5)*5
last_episode_tick = numbers[-1] - 5 #gives room for the date label
ep_nums = list(range(first_episode_tick, last_episode_tick, 5))
ep_dates = []
for episode in episodes:
    if episode['number'] in ep_nums:
        ep_dates.append(date2num(episode['date']))

dates = [date2num(episodes[0]['date'])] + ep_dates + [date2num(episodes[-1]['date'])]
tick_labels = [episodes[0]['date'].strftime("%d/%m/%Y")] + ep_nums + [episodes[-1]['date'].strftime("%d/%m/%Y")]
cbar = plt.colorbar()
cbar.set_ticks(dates)
cbar.ax.set_yticklabels(tick_labels)
cbar.ax.set_ylabel('Episode Release Date', rotation=270)

#line of best fit
#plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)), linestyle=':')

#label extreme points
label_points = sorted(zip(x, y, numbers, episodes), reverse=True)[:5]
label_points.extend(sorted(zip(x, y, numbers, episodes))[:3])
label_points.extend(sorted(zip(x, y, numbers, episodes), key=lambda x: x[1], reverse=True)[:3])
label_points.extend(sorted(zip(x, y, numbers, episodes), key=lambda x: x[1])[:3])
for x_, y_, label, ep in label_points:
    print(f"\n{ep['number']}\n{ep['title']}\nduration: {ep['length']}\nlink: {ep['link']}")
    if label == -1:
        plt.annotate(ep['title'][:13], (x_, y_))
        continue

    plt.annotate(str(label), (x_, y_))

#work our the correlation
corr = np.corrcoef(x, y)[0, 1]
print(f'correlation: {corr}')

plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.title(title)
plt.savefig('graph.png')
