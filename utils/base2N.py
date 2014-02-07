#!/usr/bin/env python
# coding: utf-8
# author: 04
# create_at:  2014-02-07 17:22:50
# vim: set noexpandtab tabstop=4 shiftwidth=4 softtabstop=4:

"""

"""

def baseN(num,b, base="0123456789abcdefghijklmnopqrstuvwxyz"):
	return ((num == 0) and  base[0] ) or ( baseN(num // b, b, base).lstrip(base[0]) + base[num % b])

def base56(num, b=56):
	return baseN(num, b, "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

def baseN2D(num_str, b, base="0123456789abcdefghijklmnopqrstuvwxyz"):
	if not num_str or num_str == base[0]:
		return 0
	curr = base.index(num_str[0])
	for i in num_str[:-1]:
		curr *= b
		curr += base.index(i)
	return curr
