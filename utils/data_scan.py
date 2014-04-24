#!/usr/bin/env python
# coding: utf-8
# author: tvboxme@gmail.com
# create_at:  2014-04-24 11:33:01
# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4:

"""

"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import datetime
from pprint import pprint

date_fmt = '%Y-%m-%d %H:%M:%S'


class paged_scan(object):
    '''  scan mongodb with recounnection.
    debug for test callback
    start for start record count
    '''

    def __init__(self, collection, query={}, pagination_by=200, reverse=False, callback=None):
        object.__init__(self)
        self.collection = collection
        self.query = query
        self.pagination_by = pagination_by
        self.reverse = reverse
        self.callback = callback

    def __call__(self, func):

        def decorator(*args, **kwargs):
            self.auto_reconnect(func, *args, **kwargs)

        return decorator

    def auto_reconnect(self, func, *args, **kwargs):
        debug = kwargs.get('debug', False)
        start = kwargs.get('start', 0)
        start_time = datetime.datetime.now()
        collection = self.collection
        pagination_by = self.pagination_by
        print 'start scan %s at %s' % (collection.full_name, start_time.strftime(date_fmt))
        total_count = collection.count()
        print 'all count: %s' % total_count
        min_page = start / pagination_by
        max_page = total_count / pagination_by + 1
        trans_data = {}
        for page in range(min_page, max_page):
            print 'start new cursor skipping %s ************************ %s' % (
                    pagination_by * page, datetime.datetime.now().strftime(date_fmt))
            cursor = (collection.find(self.query)
                    .skip(pagination_by * page)
                    .limit(pagination_by)
                    .sort('_id', int(self.reverse))
                    )
            for data in cursor:
                try:
                    func(data, trans_data, * args, **kwargs)
                except Exception:
                    break
            has_data = self.descrip_result(trans_data)
            if debug and has_data:
                break
        end_time = datetime.datetime.now()
        print 'finish scan %s at %s' % (collection.full_name, end_time.strftime(date_fmt))
        print 'duration %s' % (end_time - start_time)

        if callable(self.callback):
            self.callback(trans_data)
        else:
            self.descrip_result(trans_data)

    def descrip_result(self, trans_data, detail=False):
        has_data = {}
        for key, value in trans_data.items():
            if value:
                has_data[key] = True
            if isinstance(value, (list, )):
                print '%s(list length: %s)' % (key, len(value))
            elif isinstance(value, (dict, )):
                print '%s(dict contains: %s)' % (key, len(value.keys()))
            elif isinstance(value, (basestring, )):
                print '%s(string length: %s)' % (key, len(value))
            else:
                print '%s(%s)' % (key, type(value))
            if detail:
                pprint(value)
        return has_data
