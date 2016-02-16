#!/usr/bin/env python
import matplotlib as mpl
mpl.use('Agg')

import os
import sys
import cgi
import cgitb
import json
from python.adeireader import ADEIReader
from python.adeihelper import start_of_day, utc_timestamp
from python.hatpro import read_server_config, read_sensor_config, read_sensor_axis2
import matplotlib.pyplot as plt
import matplotlib.cm as cm


config_server = './config/server.ini'
config_sensor = './config/hatpro.ini'
output_path = './cache'
fname_tmpl = 'hatpro_time_{servername}_{sensorname}_{timestamp}.json'


def get_contour(servername, sensorname, date=None):

    # parse config
    adeihost, adeiserver, dbname = read_server_config(config_server, servername)
    groupname, sensor_readable_name, axis2_length = read_sensor_config(config_sensor, sensorname)
    axis2_unit, axis2_value = read_sensor_axis2(config_sensor, sensorname)

    print adeihost, adeiserver, dbname
    print groupname, sensor_readable_name, axis2_length

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

    # fetching data from ADEI
    fetched = adei.query_data(groupname, sensorfullname, window=window, resample=10)
    time = fetched['timestamp']
    data = [ map(float, fetched[i]) for i in sensorfullname ]

    # generate contour using matplotlib plotting function
    colormap = cm.YlGnBu
    contours = plt.contourf(time, axis2_value, data, 50, cmap=colormap)

    # extract contour paths from generated data
    Paths = []
    for l, p, c in zip(contours.layers, contours.collections, contours.tcolors):
        color = mpl.colors.rgb2hex(c[0][:3])
        Paths.append({'layer': l, 'color': color, 'path': []})

        for path in p.get_paths():
            for vertex, code in zip(path.vertices, path.codes):
                if len(Paths[-1]['path']) != 0 and code == 1:
                    Paths[-1]['path'].append(None)
                    Paths[-1]['path'].append(vertex.tolist())
                else:
                    Paths[-1]['path'].append(vertex.tolist())

    # pack data in dictionary for json serizable
    processed = { "xmin": time[0], "xmax": time[-1],
                  "ymin": axis2_value[0], "ymax": axis2_value[-1],
                  "time": time, "data": Paths }

    # wite output to file
    filename = fname_tmpl.format(servername=servername,
                                 sensorname=sensorname, timestamp=ts_0)
    with open(os.path.join(output_path, filename), 'w') as f:
        json.dump(processed, f)


if __name__ == "__main__":
    #cgitb.enable()
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

    try:
        date = reqparams["date"].value
    except KeyError:
        date = None

    get_contour(server, sensor, date)

    sys.exit()
