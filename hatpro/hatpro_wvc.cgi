#!/usr/bin/env python
import os
import sys
import cgi, cgitb
import itertools
import numpy as np
import matplotlib as mpl
import matplotlib.cm as cm
import simplejson as json
import adeitools as adei
import hatpro
from hatpro import parseConfig, device_

DEBUG_ = 1

if DEBUG_:
    pass
else:
    mpl.use('webagg')
import matplotlib.pyplot as plt

class adeiReader(hatpro.adeiReader):
    def getData(self, sensorname, groupname, t0, dt):
        # find sensor in group
        sensorList = self.sensorFilter(sensorname, groupname)
        data, = [ self.getSensorData(i, groupname, t0, dt) for i in sensorList ]
        time = self.getSensorTime(i, groupname, t0, dt)

        i, = self.sensorFilter('L2A.ELEVATION.ANGLE', groupname)
        elevation = self.getSensorData(i, groupname, t0, dt)

        i, = self.sensorFilter('L2A.AZIMUTH.ANGLE', groupname)
        azimuth = self.getSensorData(i, groupname, t0, dt)

        mask1 = [0 if s == '90' else 1 for s in elevation]

        elevation =  list(itertools.compress(elevation, mask1))
        azimuth =  list(itertools.compress(azimuth, mask1))
        time =  list(itertools.compress(time, mask1))
        data = list(itertools.compress(data, mask1))

        mask2 = [1] if azimuth[0] != azimuth[1] else [0]
        mask2.extend([
            1 
            if azimuth[i] != azimuth[i+1] and azimuth[i] != azimuth[i-1] 
            else 0 
            for i in range(1, len(azimuth)-1) ])
        mask2.extend([1] if azimuth[-1] != azimuth[-2] else [0])

        azimuth = [int(s) for s in list(itertools.compress(azimuth, mask2))]
        elevation = [float(s) for s in list(itertools.compress(elevation, mask2))]
        time = list(itertools.compress(time, mask2))
        data = [float(s) for s in list(itertools.compress(data, mask2))]

        group_azimuth = []
        group_time = [] 
        group_data = []
        a = []
        t = []
        d = []
        for i in range(len(azimuth)):
            try:
                #if abs(azimuth[i] - azimuth[i+1]) > 60: 
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

#        for t in group_time:
#            print t
#        print
#        for t in group_data:
#            print t
#        print
#        for t in group_azimuth:
#            print t
 
        data_min = min([min(x) for x in group_data])
        
        #data_max = max([max(x) for x in group_data])
        data_max = 150
        data_step = (data_max-data_min)/12

        #colormap = cm.GnBu
        #colormap = cm.YlOrRd
        #colormap = cm.RdYlGn
        colormap = cm.RdYlBu
        Paths = []
        for i in range(len(group_data)):
            d = []
            a = []
            for j in range(len(group_data[i])):
                    if group_data[i][j] < data_max:
                        d.append(group_data[i][j])
                        a.append(group_azimuth[i][j])
            d = np.array([d])
            a = np.array(a)
            t = np.arange(group_time[i][0], group_time[i][0]+800, 60)
            d = (np.repeat(d, len(t), axis=0)).transpose()

            print d
            print a

            contours = plt.contourf(
                    t, a, d, 
                    levels=np.arange(data_min-data_step,data_max+data_step, data_step), 
                    cmap=colormap)

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

#
#        layers = contours.layers
#        colors = map(mpl.colors.rgb2hex,np.array(contours.tcolors)[:,0,:3])

        if DEBUG_:
            print d
            print a
            #for p in Paths:
            #    print p['layer'],
            #    print p['path'],
            print
            #print time
            plt.ylim(ymin=0)
            plt.colorbar()
            plt.show()


        return {
                "xmin": group_time[0][0], 
                "xmax": group_time[-1][-1], 
                "ymin": 0,
                "ymax": 360,
                "time": time,
                "data": Paths
               }


def main():
    # request parameters
    if DEBUG_:
        sensorName = 'L2A.ATM.WAT.VAP.CNT'
        date_ = '1d'
    else:
        reqparams = cgi.FieldStorage()
        sensorName = reqparams["id"].value
        date_ = reqparams["date"].value

    serverInfo, groupName = parseConfig(sensorName)

    # initialize adei reader
    adei_ = adeiReader()
    adei_.setup(
            serverInfo['db_name'], 
            serverInfo['db_server'], 
            serverInfo['db_host']) 
    (t0, update) = adei_.dostuff(groupName, sensorName+'.PRF', date_)
    update = 1

    filename = "../cache/%s.%s.%s.json" % (
            device_, sensorName+'.PRF', t0)
    symbolicname = "../cache/%s.%s.%s.json" % (
            device_, sensorName+'.PRF', date_)

    # update !
    if update:
        res = adei_.getData(sensorName, groupName, t0, 86400)
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

