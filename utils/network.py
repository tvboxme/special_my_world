#!/usr/bin/env python
# coding: utf-8
# author: 04
# create_at:  2013-10-13 13:53:50
# vim: set noexpandtab tabstop=4 shiftwidth=4 softtabstop=4:

""" 网络有关工具


"""

from ipaddr import IPNetwork
from consts import ip_pattern, section_pattern


class IPSection(object):
	''' IP段操作
	'''

	def __init__(self, ip_list):
		ip_sections = {}
		for i in ip_list:
			desc = self.get_desc(i)
			self.combine_head(ip_sections, desc)
		self.ip_sections = ip_sections

	def __contains__(self, ip):
		'''  test ip in IPSection
		'''
		reg = ip_pattern.match(ip)
		if not reg:
			return False
		reg_dict = reg.groupdict()
		ip_addr = reg_dict['addr']
		ip_data = self.ip_sections.get(reg_dict['head'])
		if not ip_data:
			return False
		for addr in ip_data['addr']:
			if isinstance(addr, tuple):
				if int(addr[0]) <= int(ip_addr) <= int(addr[1]):
					return True
			elif isinstance(addr, str):
				if ip_addr == addr:
					return True
		return False

	def combine_head(self, section, desc):
		''' 将不同 desc 合并
		'''
		if not desc:
			return
		elif desc.get('head') and desc['head'] not in section:
			section.update({desc['head']: desc['addr']})
		else:
			section[desc['head']] += desc['addr']

	def get_desc(self, ip_name):
		''' 通过匹配确认是单个IP或者是IP段并返回描述字典
		'''
		_section = section_pattern.match(ip_name)
		_ip = ip_pattern.match(ip_name)
		if _section:
			ret_dict = _section.groupdict()
			ret = {
					'head': ret_dict['head'],
					'addr': [(ret_dict['start'], ret_dict['end'])]
					}
		elif _ip:
			ret_dict = _ip.groupdict()
			ret = {
					'head': ret_dict['head'],
					'addr': [ret_dict['addr']]
					}
		else:
			ret = {}
		return ret

	def get_masked_ip_section(self):
		''' 将已有ip段转换为mask方式
		'''
		def _insert_prefix_32(_keeper, head, tail):
			_make_up = '%s.%s' % (head, tail)
			ipobj = IPNetwork(_make_up)
			if ipobj not in _keeper['32']:
				_keeper['32'].append(ipobj)
			
		out = []
		for head, tails in self.ip_sections.items():
			_keeper = {'32': []}
			for tail in tails:
				if isinstance(tail, basestring):
					_insert_prefix_32(_keeper, head, tail)
				if isinstance(tail, tuple):
					start, end = tail
					for i in range(int(start), int(end)+1):
						_insert_prefix_32(_keeper, head, i)
			for prefixlen in reversed(range(1, 33)):
				fatherlen = str(prefixlen - 1)
				prefixlen = str(prefixlen)
				if not _keeper[prefixlen]:
					break
				ip_list = _keeper[prefixlen]
				for network in ip_list[:]:
					if network not in ip_list:
						continue
					father = network.supernet()
					brothers = father.subnet()
					brother = [i for i in brothers if i != network][0]
					if brother in ip_list:
						ip_list.remove(network)
						ip_list.remove(brother)
						_keeper.setdefault(fatherlen, [])
						_keeper[fatherlen].append(network.supernet())
			out.append({head: _keeper})
		return out






