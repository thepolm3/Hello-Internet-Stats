"""Contains classes related to podcasts"""

class Podcast(object):
	"""A podcast object, featuring dynamic indexing based on the sorting field"""

	def __init__(self, name, episodes, sortBy=None):
		self.episodes = episodes
		self.name = name
		self._current_sort = sortBy
		if sortBy is not None:
			self.sort(sortBy)

	def sort(self, key=None, reverse=False):
		"""sorts the podcasts by a given key. The sort is saved and used for defaul values"""
		if key is None:
			key = self._current_sort

		if key is None:
			return

		if isinstance(key, str):
			key_ = lambda ep: ep[key]
		else:
			key_ = key

		self.episodes = sorted(self.episodes, key=key_, reverse=reverse)
		self._current_sort = key

		return self

	@property
	def attributes(self, attrb=None):
		"""pod.attributes returns a list of all attributes of any episode"""
		attribs = set()
		for episode in self.episodes:
			for key in episode.keys():
				attribs.add(key)
		return attribs

	def episode_attributes(self, attrb):
		"""Gets an attribute from all episodes, e.g pod.attributes('length') returns length of all episodes"""
		for episode in self.episodes:
			if attrb in episode:
				yield episode[attrb]
			else:
				yield None

	def add_episode(self, episode):
		"""Adds an episode to the podcast. This may not be added at the end, depending on the current sort"""
		self.episodes.append(episode)
		self.sort()

	def find(self, return_index=False, **search_dict):
		"""finds all episodes matching the given terms

		pod.find(title='the worst episode ever')
		pod.find(length=3)
		"""

		for i, episode in enumerate(self.episodes):
			for attrib, value in search_dict.items():
				if episode[attrib] != value:
					break
			else:
				if return_index:
					yield i
				else:
					yield episode

	def __iter__(self):
		return iter(self.episodes)

	def __str__(self):
		return self.name

	def __repr__(self):
		return f"Podcast({self.name})"

	def __len__(self):
		return len(self.episodes)

	def __contains__(self, index):
		if len(list(self.find(**{self._current_sort:index}))) == 0:
			return False

		return True

	def __getitem__(self, index):
		items = list(self.find(**{self._current_sort:index}))

		if len(items) == 0:
			raise KeyError(f"No episode with index {index}")

		if len(items) > 1:
			raise KeyError(f"Too many episodes with index {index}")
		
		return items[0]


	def __delitem__(self, index):
		items = list(self.find(return_index=True, **{self._current_sort:index}))

		if len(items) == 0:
			raise KeyError("No episode with that specification")

		if len(items) > 1:
			raise KeyError("Too many episodes matching that description")
		
		del self.episodes[items[0]]

class Episode(object):
	"""A podcast episode object"""

	def __init__(self, **attributes):
		super(Episode, self).__setattr__('_attributes',attributes)

	def update(self, episode=None, **attributes):
		"""Updates the podcast episode with new details"""
		if episode is not None:
			if isinstance(episode, Episode):
				self._attributes.update(episode._attributes)
			else:
				self._attributes.update({'episode':episode})
		self._attributes.update(attributes)

	def keys(self):
		"""gets the attribute keys from the episode"""
		return self._attributes.keys()

	def __contains__(self, attrib):
		return (attrib in self._attributes)

	def __getattr__(self, name):
		if name in self._attributes:
			return self._attributes[name]

		return None

	def __setattr__(self, name, value):
		self._attributes[name] = value
		

	def __len__(self):
		if 'length' in self._attributes:
			return self._attributes['length']
		else:
			return 0

	def __setitem__(self, key, value):
		self._attributes[key] = value

	def __getitem__(self, key):
		if key in self._attributes:
			return self._attributes[key]

		return None

if __name__ == '__main__':
	#setting up a podcast
	ep1 = Episode(number=1, name='the best episode ever')

	#you can change an episodes attributes on the fly in two ways, the first is preferable
	ep1.host = 'John Doe'
	ep1['length'] = 2

	ep2 = Episode(number=2, name='the worst episode ever', host='Jane Doe',length=3)

	#you can also pass in a dictionary in the standard way
	episode_dict = {'name':'episode 3', 'length':3, 'host':'John Doe'}
	ep3 = Episode(number=3, **episode_dict)

	#sortBy is important since it forms the basis of indexing
	pod = Podcast('the unfinished podcast',[ep1,ep2,ep3], sortBy='number')

	#adding an episode after the factt
	pod.add_episode(Episode(number=4, name='what a world we live in'))

	#you can acess an episode by the sort value
	print(pod[1] == ep1)

	#alternatively use pod.find to get a list of values
	print(list(pod.find(name='episode 3'))[0].length)

	#you can search for specific episodes by any category
	print([ep.name for ep in pod.find(length=3)])

	#checking if episode 1 has the length attribute
	if 'length' in ep1:
		print('ep1 has a defined length')

	else:
		print('ep1 does not have a defined length')
	
	print()

	#you can loop through podcast episodes like so
	for ep in pod:
		print(f"{ep.name} by {ep.host}")

	print()

	#you can choose to resort the podcast
	pod.sort('name')

	#pod[1] now throws an error, since it is indexed by title
	print(pod['episode 3'])

	for ep in pod:
		print(ep.name)
	
	print()

	pod.sort('number')


	pod.add_episode(Episode(number=5, name='Oops we missed one'))

	#this is how we remove an episode
	del pod[5]

	#This is how we can update a previous episode
	pod[1].update(name='The very first episode')

	for ep in pod:
		print(f"{ep.number}: {ep.name}")

	print()

	#we can get the attributes of the podcast from pod.attributes
	for attribute in pod.attributes:

		#we can get a list of the attributes by episode from episode_attributes
		print(list(pod.episode_attributes(attribute)))

	#a key that is missing will always return None
	print(ep1.hairstyle)
	print(list(pod.episode_attributes('hairstyle')))
