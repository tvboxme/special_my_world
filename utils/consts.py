#!/usr/bin/env python
# coding: utf-8
# author: 04
# create_at:  2013-10-13 15:32:30
# vim: set noexpandtab tabstop=4 shiftwidth=4 softtabstop=4:

"""

"""

import re

# pattern consts
SECTION_PATTERN = r'^(?P<head>\d{1,3}\.\d{1,3}\.\d{1,3})\.(?P<start>\d{1,3})\-(?P<end>\d{1,3})$'
section_pattern = re.compile(SECTION_PATTERN) 
IP_PATTERN = r'^(?P<head>\d{1,3}\.\d{1,3}\.\d{1,3})\.(?P<addr>\d{1,3})$'
ip_pattern = re.compile(IP_PATTERN)
