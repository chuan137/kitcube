#!/usr/bin/env python
# -*- coding: utf-8 -*-
from adeihelper import query_csv, query_xml, adei_timestamp

DEBUG = 1


class AdeiError(Exception):
    'not implemented'
    def __init__(self, message, errors):

        super(AdeiError, self).__init__(message)
        self.errors = errors


class ADEIReader(object):

    def __init__(self, host, server, db):
        self.host = host + '/services/'
        self.server = server
        self.db = db

        self._groups = []
        self._sensors = {}
        self.update_group_list()

    def qurl(self, qtype, **kargs):
        url = self.host

        if qtype == 'get':
            url = url + 'getdata.php?'
        elif qtype == 'group':
            url = url + 'list.php?target=groups'
        elif qtype == 'sensor':
            url = url + 'list.php?target=items'

        kargs['db_server'] = self.server
        kargs['db_name'] = self.db
        kargs['window'] = kargs.get('window') or '-1'
        kargs['resample'] = kargs.get('resample') or '0'
        for k, v in kargs.iteritems():
            url += '&' + k + '=' + v

        if DEBUG:
            print url
        return url

    def update_group_list(self):
        url = self.qurl('group')
        self._groups = query_xml(url)

    def update_sensor_list(self, groupname, force=False):
        url = self.qurl('sensor', db_group=groupname)
        self._sensors[groupname] = { v['name']:v['value'] for v in  query_xml(url) }

    def query_data(self, group, sensors):
        ' Fetch data from ADEI server. '
        if not isinstance(sensors, list):
            sensors = [ sensors ]
        if group not in self._sensors:
            self.update_sensor_list(group)

        try:
            masks = map(int, sensors)
        except:
            masks = map(self._sensors.get(group).get, sensors)
            masks = map(int, masks)

        if masks:
            masks = sorted(masks)
            try:
                data = self._query(group, *masks)
                data[0] = ('timestamp', adei_timestamp(data[0][1]))
            except:
                data = []
        else:
            data = []
        return data

    def _query(self, group, *masks):
        masks = ','.join(map(str, masks))
        url = self.qurl('get', db_group=group, db_mask=masks)
        return query_csv(url)

    @property
    def sensors(self):
#        if not self._sensors:
#            print 'retrieve sensor list'
#            self._sensors = self.get_sensor_list()
        return self._sensors

    @property
    def groups(self):
        return self._groups

