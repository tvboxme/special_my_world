#!/usr/bin/env python
# coding: utf-8
# author: 04
# create_at:  2013-12-03 16:52:19
# vim: set noexpandtab tabstop=4 shiftwidth=4 softtabstop=4:

"""

"""
import requests
import xml.etree.ElementTree as ET


def get_alexa_rank(url):
    popularity_rank = '-'
    reach_rank = '-'

    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31'}

    req = 'http://data.alexa.com/data?cli=10&dat=snbamz&url=%s' % (url)

    try:
        data = requests.get(url=req, timeout=5, headers=header)
        et = ET.fromstring(data.content)

        if et.findall('.//POPULARITY[@TEXT]'):
            popularity_rank = et.findall('.//POPULARITY[@TEXT]')[0].get('TEXT')
            popularity_rank = int(popularity_rank)

        if et.findall('.//COUNTRY[@RANK]'):
            reach_rank = et.findall('.//COUNTRY[@RANK]')[0].get('RANK')
            reach_rank = int(reach_rank)

    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception ,e :
        pass

    return popularity_rank, reach_rank


if '__main__' == __name__:
	print get_alexa_rank('jiasule.com')

