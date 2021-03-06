#!/usr/bin/env python
# coding: utf-8
# author: 04
# create_at:  2013-10-11 23:48:58
# vim: set noexpandtab tabstop=4 shiftwidth=4 softtabstop=4:

""" 服务类线程常用工具

"""

import time
import sys

class AbsolutelyTimer(object):

	def __init__(self, sleep_second):
		self.__sleep_second = sleep_second
		self.last_wake = 0

	def __get_time(self):
		if sys.platform == 'win32':
			return time.clock()
		else:
			return time.time()
		
	def sleep(self):
		last_wake = self.last_wake
		now = self.__get_time()
		if last_wake:
			delay = now - last_wake
			if self.__sleep_second > delay:
				time.sleep(self.__sleep_second - delay)
		else:
			time.sleep(self.__sleep_second)
		self.last_wake = self.__get_time()
		return now



def test_absolutely_timer():
	sleep = 1
	time_list = []
	timer = AbsolutelyTimer(sleep)
	for i in range(20):
		time_list.append(time.time())
		timer.sleep()
		if i>0:
			print i, time_list[i], time_list[i-1], time_list[i] - time_list[i-1]
	time_list.append(time.time())
	i += 1
	print i, time_list[i], time_list[i-1], time_list[i] - time_list[i-1]
	print 'avg:', (time_list[-1] - time_list[0]) / 20

if "__main__" == __name__:
	test_absolutely_timer()
