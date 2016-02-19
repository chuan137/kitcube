#!/usr/bin/env python
import sys
sys.path.insert(0, '../')

import os
import cgi, cgitb
import numpy as np
import json
from python.adeireader import ADEIReader
from python.adeihelper import start_of_day, utc_timestamp
from python.hatpro import read_server_config, read_sensor_config

basepath = os.path.dirname(__file__)

config_server = os.path.join(basepath, '../config/server.ini')
config_sensor = os.path.join(basepath, '../config/hatpro.ini')
output_path = os.path.join(basepath, './cache')
fname_tmpl = 'hatpro_time_{servername}_{sensorname}_{timestamp}.json'


def get_time_series(servername, sensorname, date=None):

    # parse config
    adeihost, adeiserver, dbname = read_server_config(config_server, servername)
    groupname, sensor_readable_name, axis2_length = read_sensor_config(config_sensor, sensorname)

    # initialize adei
    adei = ADEIReader(adeihost, adeiserver, dbname)
    if groupname not in adei.sensors:
        adei.update_sensor_list(groupname)

    # when sensor has second axis, generate sensor list <sensorname>.001, ...
    if axis2_length == 1:
        sensorfullname = '{} {}'.format(sensorname, sensor_readable_name)
    else:
        sensorfullname = ['{}.{:03d} {}'.format(sensorname, i, sensor_readable_name)
                          for i in range(axis2_length)]

    # set time window for the whole day, either from give date,
    # or the last available day
    if date:
        year, month, day = map(int, date.split('-'))
        ts_0 = utc_timestamp(year, month, day)
        window = '%d-%d' % (ts_0, ts_0+86400)
    else:
        # fetch last data to decide date
        fetched_data = adei.query_data(groupname, sensorfullname)
        laststamp = fetched_data['timestamp'][-1]
        ts_0 = start_of_day(laststamp)
        window = '%d-%d' % (ts_0, laststamp)

    # fetch data
    fetched_data = adei.query_data(groupname, sensorfullname, window=window, resample=60)

    # format data
    fetched_data = {'timestamp': fetched_data['timestamp'], \
                    'data': [ v for k,v in fetched_data.iteritems() if k != 'timestamp' ]}

    filename = fname_tmpl.format(servername=servername, sensorname=sensorname, timestamp=ts_0)
    with open(os.path.join(output_path, filename), 'w') as f:
        json.dump(fetched_data, f)


if __name__ == "__main__":

    cgitb.enable()
    content_type = 'text/plain; charset="UTF-8"'
    sys.stdout.write('Content-type: %s\n\n' % content_type)

    # request parameters
    reqparams = cgi.FieldStorage()

    try:
        server = reqparams["server"].value
    except KeyError:
        server = 'HEADS'

    try:
        sensor = reqparams["sensor"].value
    except KeyError:
        sensor = 'L2A.ATM.WAT.VAP.CNT'
        sensor = 'L2A.ATM.LIQ.WAT.CNT'
        sensor = 'L1B.BRIGHT.TEMP.IR'
        sensor = 'L1B.BRIGHT.TEMP'

    # date format: '2014-12-6'
    try:
        date = reqparams["date"].value
    except KeyError:
        date = None

    get_time_series(server, sensor, date)

