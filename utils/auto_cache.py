#!/usr/bin/env python
# coding: utf-8
# author: 04
# create_at:  2013-12-06 16:07:21
# vim: set noexpandtab tabstop=4 shiftwidth=4 softtabstop=4:

""" 节约是美德

DB瞬时缓冲器

"""
import time

class AutoCache(object):
	''' cache_time is seconds for update cycle
		normally cache_time should lower than 5 seconds.
	'''
	def __init__(self, cache_time):
		object.__init__(self)
		self.cache_time = cache_time
		self.cache_value = None
		self.next_sync = None
	
	def __call__(self, func):
		now = time.time()
		should_sync = not self.next_sync or not cache_value or now > self.next_sync
		self.next_sync = now + self.cache_time
		def inner(*args, **kwargs):
			if should_sync:
				self.cache_value = func(*args, **kwargs)
			return self.cache_value

		return inner
