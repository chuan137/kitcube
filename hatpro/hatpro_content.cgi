#!/usr/bin/env python
import sys
import os
import cgi
import cgitb
import json
import itertools
import numpy as np
import matplotlib as mpl; mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm

basepath = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
sys.path.insert(0, basepath)

from python.adeireader import ADEIReader
from python.adeihelper import start_of_day, utc_timestamp
from python.hatpro import *

config_server = os.path.join(basepath, './config/server.ini')
config_sensor = os.path.join(basepath, './config/hatpro.ini')
output_path = os.path.join(basepath, './hatpro/cache')
fname_tmpl = 'hatpro_content_{servername}_{sensorname}.PRF_{timestamp}.json'


def get_content(servername, sensorname, date=None):

    # parse config
    adeihost, adeiserver, dbname = read_server_config(config_server, servername)
    groupname, sensor_readable_name, axis2_length = read_sensor_config(config_sensor, sensorname)

    # initialize adei
    adei = ADEIReader(adeihost, adeiserver, dbname)
    if groupname not in adei.sensors:
        adei.update_sensor_list(groupname)

    sensorfullname = '{} {}'.format(sensorname, sensor_readable_name)

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

    # query data
    sensor_list = [sensorfullname, 'L2A.ELEVATION.ANGLE elevation_angle', 'L2A.AZIMUTH.ANGLE azimuth_angle']
    fetched = adei.query_data(groupname, sensor_list, window=window, resample=60)

    time = fetched['timestamp']
    elevation = map(float, fetched['L2A.ELEVATION.ANGLE elevation_angle'])
    azimuth = map(int, fetched['L2A.AZIMUTH.ANGLE azimuth_angle'])
    data = map(float, fetched[sensorfullname])

    mask1 =   np.array(elevation) != 90.0

    elevation =  list(itertools.compress(elevation, mask1))
    azimuth =  list(itertools.compress(azimuth, mask1))
    time =  list(itertools.compress(time, mask1))
    data = list(itertools.compress(data, mask1))

    if len(azimuth) > 0:
        mask2 = [1] if azimuth[0] != azimuth[1] else [0]
        mask2.extend([
                1 
                if azimuth[i] != azimuth[i+1] and azimuth[i] != azimuth[i-1] 
                else 0 
                for i in range(1, len(azimuth)-1) ])
        mask2.extend([1] if azimuth[-1] != azimuth[-2] else [0])

        azimuth = list(itertools.compress(azimuth, mask2))
        elevation = list(itertools.compress(elevation, mask2))
        time = list(itertools.compress(time, mask2))
        data = list(itertools.compress(data, mask2))

    if len(data) == 0:
        return

    group_azimuth = []
    group_time = [] 
    group_data = []
    a = []
    t = []
    d = []
    for i in range(len(azimuth)):
        try:
            if abs(time[i]-time[i+1]) > 100:
                a.append(azimuth[i])
                t.append(time[i])
                d.append(data[i])
                group_azimuth.append(a)
                group_time.append(t)
                group_data.append(d)
                a = []
                t = []
                d = []
            else:
                a.append(azimuth[i])
                t.append(time[i])
                d.append(data[i])
        except:
            a.append(azimuth[i])
            t.append(time[i])
            d.append(data[i])
            group_azimuth.append(a)
            group_time.append(t)
            group_data.append(d)

    data_min = min([min(x) for x in group_data])
    data_max = max([max(x) for x in group_data])
    data_step = (data_max-data_min)/12

    colormap = cm.RdYlBu
    Paths = []
    for i in range(len(group_data)):
        d = np.array([group_data[i]])
        t = np.arange(group_time[i][0], group_time[i][0]+800, 60)
        a = [360 if x==0 else x for x in group_azimuth[i]]
        d = (np.repeat(d, len(t), axis=0)).transpose()

        contours = plt.contourf(
                t, a, d, 
                levels=np.arange(data_min-data_step,data_max+data_step, data_step), 
                cmap=colormap)

        plt.show()

        for l, p, c in zip(
                contours.layers, 
                contours.collections, 
                contours.tcolors):
            color = mpl.colors.rgb2hex(c[0][:3])
            for path in p.get_paths():
                pp = []
                for vertex, code in zip(path.vertices, path.codes):
                    if len(pp) != 0 and code == 1:
                        pp.append(None)
                        pp.append(vertex.tolist())
                    else:
                        pp.append(vertex.tolist())

                Paths.append({"layer": l, "path": pp, "color": color})

    processed =  { "xmin": group_time[0][0],
                   "xmax": group_time[-1][-1],
                   "ymin": 0,
                   "ymax": 360,
                   "time": time,
                   "data": Paths }

    filename = fname_tmpl.format(servername=servername,
                                 sensorname=sensorname, timestamp=ts_0)
    with open(os.path.join(output_path, filename), 'w') as f:
        json.dump(processed, f)


if __name__ == "__main__":
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

    try:
        date = reqparams["date"].value
    except KeyError:
        date = None

    get_content(server, sensor, date)

    sys.exit()

#
# class adeiReader(hatpro.adeiReader):
#     def getData(self, sensorname, groupname, t0, dt):
#         # find sensor in group
#         sensorList = self.sensorFilter(sensorname, groupname)
#         data, = [ self.getSensorData(i, groupname, t0, dt) for i in sensorList ]
#         time = self.getSensorTime(i, groupname, t0, dt)
#
#         i, = self.sensorFilter('L2A.ELEVATION.ANGLE', groupname)
#         elevation = self.getSensorData(i, groupname, t0, dt)
#
#         i, = self.sensorFilter('L2A.AZIMUTH.ANGLE', groupname)
#         azimuth = self.getSensorData(i, groupname, t0, dt)
#
#         mask1 = [0 if s == '90' else 1 for s in elevation]
#
#         elevation =  list(itertools.compress(elevation, mask1))
#         azimuth =  list(itertools.compress(azimuth, mask1))
#         time =  list(itertools.compress(time, mask1))
#         data = list(itertools.compress(data, mask1))
#
#         mask2 = [1] if azimuth[0] != azimuth[1] else [0]
#         mask2.extend([
#             1 
#             if azimuth[i] != azimuth[i+1] and azimuth[i] != azimuth[i-1] 
#             else 0 
#             for i in range(1, len(azimuth)-1) ])
#         mask2.extend([1] if azimuth[-1] != azimuth[-2] else [0])
#
#         azimuth = [int(s) for s in list(itertools.compress(azimuth, mask2))]
#         elevation = [float(s) for s in list(itertools.compress(elevation, mask2))]
#         time = list(itertools.compress(time, mask2))
#         data = [float(s) for s in list(itertools.compress(data, mask2))]
#
#         group_azimuth = []
#         group_time = [] 
#         group_data = []
#         a = []
#         t = []
#         d = []
#         for i in range(len(azimuth)):
#             try:
#                 #if abs(azimuth[i] - azimuth[i+1]) > 60: 
#                 if abs(time[i]-time[i+1]) > 100:
#                     a.append(azimuth[i])
#                     t.append(time[i])
#                     d.append(data[i])
#                     group_azimuth.append(a)
#                     group_time.append(t)
#                     group_data.append(d)
#                     a = []
#                     t = []
#                     d = []
#                 else:
#                     a.append(azimuth[i])
#                     t.append(time[i])
#                     d.append(data[i])
#             except:
#                 a.append(azimuth[i])
#                 t.append(time[i])
#                 d.append(data[i])
#                 group_azimuth.append(a)
#                 group_time.append(t)
#                 group_data.append(d)
#
# #        for t in group_time:
# #            print t
# #        print
# #        for t in group_data:
# #            print t
# #        print
# #        for t in group_azimuth:
# #            print t
#  
#         data_min = min([min(x) for x in group_data])
#         data_max = max([max(x) for x in group_data])
#         data_step = (data_max-data_min)/12
#         #data_min = int(data_min/20) * 20
#         #data_max = int(data_max/20+1) * 20
#         #print data_min, data_max
#
#         #colormap = cm.GnBu
#         #colormap = cm.YlOrRd
#         #colormap = cm.RdYlGn
#         colormap = cm.RdYlBu
#         Paths = []
#         for i in range(len(group_data)):
#             d = np.array([group_data[i]])
#             t = np.arange(group_time[i][0], group_time[i][0]+800, 60)
#             a = [360 if x==0 else x for x in group_azimuth[i]]
#             d = (np.repeat(d, len(t), axis=0)).transpose()
#
#             contours = plt.contourf(
#                     t, a, d, 
#                     levels=np.arange(data_min-data_step,data_max+data_step, data_step), 
#                     cmap=colormap)
#
#             for l, p, c in zip(
#                     contours.layers, 
#                     contours.collections, 
#                     contours.tcolors):
#                 color = mpl.colors.rgb2hex(c[0][:3])
#                 for path in p.get_paths():
#                     pp = []
#                     for vertex, code in zip(path.vertices, path.codes):
#                         if len(pp) != 0 and code == 1:
#                             pp.append(None)
#                             pp.append(vertex.tolist())
#                         else:
#                             pp.append(vertex.tolist())
#
#                     Paths.append({"layer": l, "path": pp, "color": color})
#
# #
# #        layers = contours.layers
# #        colors = map(mpl.colors.rgb2hex,np.array(contours.tcolors)[:,0,:3])
#
#         if DEBUG_:
#             print d
#             print a
#             #for p in Paths:
#             #    print p['layer'],
#             #    print p['path'],
#             print
#             #print time
#             plt.ylim(ymin=0)
#             plt.colorbar()
#             plt.show()
#
#
#         return {
#                 "xmin": group_time[0][0], 
#                 "xmax": group_time[-1][-1], 
#                 "ymin": 0,
#                 "ymax": 360,
#                 "time": time,
#                 "data": Paths
#                }
#


