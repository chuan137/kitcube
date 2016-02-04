#!/usr/bin/env python
import os
import sys
import cgi, cgitb
import numpy as np
import simplejson as json
import adeitools as adei
import hatpro
from hatpro import parseConfig, device_

class adeiReader(hatpro.adeiReader):
    def getData(self, sensorname, groupname, t0, dt):
        # find sensor in group
        sensorList = self.sensorFilter(sensorname, groupname)
        data = [ self.getSensorData(i, groupname, t0, dt) for i in sensorList ]
        time = self.getSensorTime(i, groupname, t0, dt)

        i, = self.sensorFilter('L2A.ELEVATION.ANGLE', groupname)
        elevation = self.getSensorData(i, groupname, t0, dt)
        elevation90 = [1 if s=='90' else 0 for s in elevation]

        data = [[y for x,y in zip(elevation, dd) if x=='90'] for dd in data]
        time = [y for x,y in zip(elevation, time) if x=='90']

        res = {}
        res['axis_unit'] = [None]
        res['axis2_unit'] = [None]
        res['axis2_values'] = [None]

        # slice data when amount of data is too large
        #factor = int(len(data)*len(data[0])/(time[-1] - time[0])/0.2 + 0.5)
        #if factor > 1:
        #    time = time[::factor]
        #    data = [ x[::factor] for x in data ]
        #    #factor = len(data)*len(data[0])/float(time[-1] - time[0])
        #    #print factor
        res['time'] = time
        res['data'] = data

        return res

def main():
    # request parameters
    reqparams = cgi.FieldStorage()
    #sensor_ = reqparams["id"].value
    #date_ = reqparams["date"].value
    sensorName = 'L2A.ATM.WAT.VAP.CNT'
    date_ = '0d'

    serverInfo, groupName = parseConfig(sensorName)

    # initialize adei reader
    adei_ = adeiReader()
    adei_.setup(
            serverInfo['db_name'], 
            serverInfo['db_server'], 
            serverInfo['db_host']) 
    (t0, update) = adei_.dostuff(groupName, sensorName, date_)

    filename = "./cache/%s.%s.%s.json" % (
            device_, sensorName, t0)
    symbolicname = "./cache/%s.%s.%s.json" % (
            device_, sensorName, date_)

    # update !
    if update:
        res = adei_.getData(sensorName, groupName, t0, 86400)
        with  open(filename, "w") as f:
            json.dump(res, f)

    # create symbolic name
    try:
        os.symlink(filename, symbolicname)
    except OSError:
        os.remove(symbolicname)
        os.symlink(filename, symbolicname)




if __name__ == "__main__":
    #cgitb.enable()
    content_type = 'text/plain; charset="UTF-8"'
    sys.stdout.write('Content-type: %s\n\n' % content_type)

    main()

    sys.exit()

