#!/usr/bin/env python
import os
import sys
import cgi, cgitb
import numpy as np
import json
from python.adeireader import ADEIReader
from python.adeihelper import start_of_day, NumpyEncoder
from python.hatpro import read_server_config, read_sensor_config

config_server = './config/server.ini'
config_sensor = './config/hatpro.ini'


def main():
    # request parameters
    # reqparams = cgi.FieldStorage()
    #sensor_ = reqparams["id"].value
    #date_ = reqparams["date"].value

    servername = 'HEADS'
    sensorname = 'L2A.ATM.WAT.VAP.CNT'
    filename = 'hatpro_time_{servername}_{sensorname}_{timestamp}.json'
    output_path = './cache'

    adeihost, adeiserver, dbname = read_server_config(config_server, servername)
    groupname, sensorfullname = read_sensor_config(config_sensor, sensorname)
    adei = ADEIReader(adeihost, adeiserver, dbname)

    fetched_data = adei.query_data(groupname, sensorfullname)
    laststamp = fetched_data['timestamp'][-1]
    ts_0 = start_of_day(laststamp)

    window = '%d-%d' % (ts_0, laststamp)
    fetched_data = adei.query_data(groupname, sensorfullname, window=window, resample=60)

    filename = filename.format(servername=servername, sensorname=sensorname, timestamp=ts_0)

    with open(os.path.join(output_path, filename), 'w') as f:
        json.dump(fetched_data, f, cls=NumpyEncoder)


if __name__ == "__main__":
    #cgitb.enable()
    content_type = 'text/plain; charset="UTF-8"'
    sys.stdout.write('Content-type: %s\n\n' % content_type)

    main()

#
# class adeiReader(hatpro.adeiReader):
#     def getData(self, sensorname, groupname, t0, dt):
#         # find sensor in group
#         sensorList = self.sensorFilter(sensorname, groupname)
#         data = [ self.getSensorData(i, groupname, t0, dt) for i in sensorList ]
#         time = self.getSensorTime(i, groupname, t0, dt)
#
#         i, = self.sensorFilter('L2A.ELEVATION.ANGLE', groupname)
#         elevation = self.getSensorData(i, groupname, t0, dt)
#         elevation90 = [1 if s=='90' else 0 for s in elevation]
#
#         data = [[y for x,y in zip(elevation, dd) if x=='90'] for dd in data]
#         time = [y for x,y in zip(elevation, time) if x=='90']
#
#         res = {}
#         res['axis_unit'] = [None]
#         res['axis2_unit'] = [None]
#         res['axis2_values'] = [None]
#
#         # slice data when amount of data is too large
#         #factor = int(len(data)*len(data[0])/(time[-1] - time[0])/0.2 + 0.5)
#         #if factor > 1:
#         #    time = time[::factor]
#         #    data = [ x[::factor] for x in data ]
#         #    #factor = len(data)*len(data[0])/float(time[-1] - time[0])
#         #    #print factor
#         res['time'] = time
#         res['data'] = data
#
#         return res
#

