#!/usr/bin/env python
import os
import sys
import cgi, cgitb
import numpy as np
import simplejson as json
import matplotlib as mpl
import matplotlib.cm as cm
import adeitools as adei
import hatpro
from hatpro import parseConfig, device_

mpl.use('Agg')
import matplotlib.pyplot as plt

class adeiReader(hatpro.adeiReader):
    def getData(self, sensorName, groupName, t0, dt):
        sensorList = self.sensorFilter(sensorName, groupName)

        colormap = cm.YlGnBu

        time = self.getSensorTime(sensorList[0], groupName, t0, dt)
        data = [ self.getSensorData(i, groupName, t0, dt) 
                for i in sensorList ]
        heights =  [int(self.groups[groupName]['sensors'][i]['axis2_value'])
                for i in sensorList]
        contours = plt.contourf(time, heights, data, 50, cmap=colormap)

        Paths = []
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

        return {
                "xmin": time[0], 
                "xmax": time[-1], 
                "ymin": heights[0], 
                "ymax": heights[-1],
                "time": time,
                "data": Paths
               }
    


def main():
    # request parameters
    reqparams = cgi.FieldStorage()
    sensorName = reqparams["id"].value
    date_ = reqparams["date"].value
    dt = 86400
    #sensorName = 'L2C.AIR.POT.TEM.PRF'
    #date_ = '0d'

    serverInfo, groupName =  parseConfig(sensorName)
    adei_ = adeiReader()
    adei_.setup(serverInfo['db_name'], 
                serverInfo['db_server'], 
                serverInfo['db_host']) 
    
    t0, update = adei_.dostuff(groupName, sensorName, date_)


    filename = "../cache/%s.%s.%s.json" % (
            device_, sensorName, t0)
    symbolicname = "../cache/%s.%s.%s.json" % (
            device_, sensorName, date_)

    if update:
        res = adei_.getData(sensorName, groupName, t0, dt)
        with  open(filename, "w") as f:
            json.dump(res, f)

    # create symbolic name
    if os.path.exists(symbolicname):
        os.remove(symbolicname)
    os.symlink(filename, symbolicname)



if __name__ == "__main__":
    #cgitb.enable()
    content_type = 'text/plain; charset="UTF-8"'
    sys.stdout.write('Content-type: %s\n\n' % content_type)

    main()

    sys.exit()

