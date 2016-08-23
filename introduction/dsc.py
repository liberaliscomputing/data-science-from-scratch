#!/usr/bin/python
# -*- coding: utf-8 -*-

import ujson as json

class DataSciencester(object):
	def __init__(self, data):
		"""
		:type data: json
		:rtype: void
		"""
		self.users = data['users']
		self.friendships = data['friendships']

	def list_friends(self):
		# create a friends list
		for user in self.users:
			user['friends'] = []
		# add friends to the list
		for i, j in self.friendships:
			self.users[i]['friends'].append(self.users[j])
			self.users[j]['friends'].append(self.users[i])

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
		num_friends_by_id = [(user['id'], self.number_of_friends(user)) for user in self.users]
		return sorted(num_friends_by_id, key=lambda (id, num_friends): num_friends, reverse=True)

if __name__ == '__main__':
	path = 'data/data.json'
	data = json.loads(open(path).read())
	dsc = DataSciencester(data)

