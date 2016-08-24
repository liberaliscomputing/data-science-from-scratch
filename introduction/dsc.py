#!/usr/bin/python
# -*- coding: utf-8 -*-

import ujson as json
from collections import Counter
from collections import defaultdict


class DataSciencester(object):
	def __init__(self, data):
		"""
		:type data: json
		:rtype: void
		"""
		self.users = data['users']
		self.friendships = data['friendships']
		self.interests = data['interests']

	def list_friends(self):
		# create a friends list
		for user in self.users:
			user['friends'] = []
		
		# add friends to the list
		for i, j in self.friendships:
			self.users[i]['friends'].append(
				{k: v for k, v in self.users[j].items() if k == 'id' or k == 'name'})
			self.users[j]['friends'].append(
				{k: v for k, v in self.users[i].items() if k == 'id' or k == 'name'})

	def number_of_friends(self, user):
	# count the number of friends
		return len(user['friends'])

	def total_connections(self):
		# count the number of connections in total
		return sum(self.number_of_friends(user) for user in self.users)

	def avg_connections(self):
		# caculate the mean number of connections
		num_users = len(self.users)
		return self.total_connections() / float(num_users)

	def num_friends_by_id(self):
		# create a sorted list of (id, num_friends) in descending order
		num_friends_by_id = [(user['id'], 
			self.number_of_friends(user)) for user in self.users]
		return sorted(num_friends_by_id, 
			key=lambda (id, num_friends): num_friends, reverse=True)

	def friends_of_friend_ids_all(self, user):
		# 'foaf' is short for 'friend of a friend'"""
		return [foaf['id'] 
			for friend in user['friends'] 
			for foaf in self.users[friend['id']]['friends']]

	def not_the_same(self, user, other):
		# two users are not the same if they have different ids
		return user['id'] != other['id']

	def not_friends(self, user, other):
		return other not in user['friends']
		"""
		return all(self.not_the_same(friend, other) 
			for friend in user['friends'])
		"""

	def friends_of_friend_ids_new(self, user):
		# find true mutual friends
		return Counter(foaf['id'] 
			for friend in user['friends'] 
			for foaf in self.users[friend['id']]['friends'] 
			if self.not_the_same(user, foaf) and self.not_friends(user, foaf))	

	def data_scientists_who_like(self, target_insterest):
		# find ids interested in target_interest
		return [user_id 
		for (user_id, interest) in self.interests 
		if interest.lower() == target_insterest.lower()]

	def user_ids_by_interest(self):
		# create a dic storing interests by user_ids
		user_ids_by_interest = defaultdict(list)
		for user_id, interest in self.interests:
			user_ids_by_interest[interest].append(user_id)
		return user_ids_by_interest

	def interests_by_user_id(self):
		# create a dic storing user_ids by interests
		interests_by_user_id = defaultdict(list)
		for user_id, interest in self.interests:
			interests_by_user_id[user_id].append(interest)
		return interests_by_user_id

	def most_common_interests_with(self, user):
		return Counter(user_id 
			for interest in self.interests_by_user_id()[user['id']]
			for user_id in self.user_ids_by_interest()[interest] 
			if user_id != user['id'])

if __name__ == '__main__':
	path = 'data/data.json'
	data = json.loads(open(path).read())
	dsc = DataSciencester(data)
	dsc.list_friends()
	print dsc.most_common_interests_with(dsc.users[0])
