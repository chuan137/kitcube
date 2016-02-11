#!/usr/bin/env python

import os
import sys
import netCDF4 as nc
from itertools import compress
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

datapath = "/home/chuan/projects/kitcube/imkcube-data/HDCP2/080/RPG/dataproc/kih/data"
cachepath = "/home/chuan/projects/kitcube/imkcube-data/HDCP2/080/RPG/cache"

def plot_timeserie(time, data, title, ylabel, path):
    plt.figure()
    plt.plot(time, data)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlim(0,24)
    plt.xticks(range(0,24,4), ['00:00','04:00','08:00','12:00','16:00','20:00'], rotation=20)
    plt.savefig(path, format='svg', bbox_inches='tight')
    plt.close()

def plot_contour(time, z, data, path, title="", ylabel=""):
    plt.figure()
    fig, ax = plt.subplots()
    cax = ax.contourf(time,z,data,100)
    fig.colorbar(cax)
    plt.savefig(plotcachepath+path+".svg", format='svg', bbox_inches='tight')
    plt.close()
 


for d in os.listdir(os.path.join(datapath,'level1')):
    files = os.listdir(os.path.join(datapath,'level1',d))
    for f in (x for x in files if x.endswith('1b.nc')):
        datestr = f[:6]
        print datestr

        l1bpath = os.path.join(datapath,'level1',d,datestr+'_kih_l1b.nc')
        l2apath = os.path.join(datapath,'level2',d,datestr+'_kih_l2a.nc')
        l2cpath = os.path.join(datapath,'level2',d,datestr+'_kih_l2c.nc')
        plotcachepath = os.path.join(cachepath,'plots',datestr)
        datacachepath = os.path.join(cachepath,'data',datestr)

        try:
            ds_lev1b = nc.Dataset(l1bpath, 'r')
            ds_lev2a = nc.Dataset(l2apath, 'r')
            ds_lev2c = nc.Dataset(l2cpath, 'r')
        except RuntimeError as err:
            if err[0] != 'No such file or directory':
                print err
            continue

        time        = ds_lev1b.variables['time'][:]
        azimuth     = ds_lev1b.variables['azimuth_angle'][:]
        elevation   = ds_lev1b.variables['elevation_angle'][:]
        brt_temp    = ds_lev1b.variables['brightness_temperature'][:]
        brt_temp_ir = ds_lev1b.variables['brightness_temperature_ir'][:]

        time2a      = ds_lev2a.variables['time'][:]
        azimuth2a   = ds_lev2a.variables['azimuth_angle'][:]
        elevation2a = ds_lev2a.variables['elevation_angle'][:]
        atm_wvc     = ds_lev2a.variables['atmosphere_water_vapor_content'][:]
        atm_lwc     = ds_lev2a.variables['atmosphere_liquid_water_content'][:]

        time2c      = ds_lev2c.variables['time'][:]
        z2c         = ds_lev2c.variables['z'][:]
        rel_hum_p   = ds_lev2c.variables['relative_humidity_profile'][:]
        air_ptemp_p = ds_lev2c.variables['air_potential_temperature_profile'][:]
        air_temp    = ds_lev2c.variables['air_temperature'][:]
        air_pres    = ds_lev2c.variables['air_pressure'][:]
        rel_hum     = ds_lev2c.variables['relative_humidity'][:]
        rel_hum_p   = ds_lev2c.variables['relative_humidity_profile'][:]

        elv90_selector = map(lambda x: x==90, elevation)
        time_90        = list(compress(time, elv90_selector))
        brt_temp_90    = list(compress(brt_temp, elv90_selector))
        brt_temp_ir_90 = list(compress(brt_temp_ir, elv90_selector))

        plot_timeserie(time_90, brt_temp_90,
                'brightness temperature',
                '[K]',
                plotcachepath+'_bt.svg')
        plot_timeserie(time_90, brt_temp_ir_90,
                'brightness temperature IR', 
                '[deg Celsius]', 
                plotcachepath+'_btir.svg')


        elv90_selector = map(lambda x: x==90, elevation2a)
        time_90        = list(compress(time2a, elv90_selector))
        atm_wvc_90     = list(compress(atm_wvc, elv90_selector))
        atm_lwc_90     = list(compress(atm_lwc, elv90_selector))

        plot_timeserie(time_90,
                       atm_wvc_90,
                       'atmosphere water vapor content',
                       '[kg/m^2]', 
                       plotcachepath+'_awvc.svg')
        plot_timeserie(time_90,
                       atm_lwc_90, 
                       'atmosphere liquid water content', 
                       '[kg/m^2]', 
                       plotcachepath+'_alwc.svg')

        plot_contour(time2c,z2c,air_ptemp_p.transpose(),'_aptp')

        plot_contour(time2c,z2c,rel_hum_p.transpose(),'_rhp')

        print azimuth2a
        print elevation2a
        sys.exit()

