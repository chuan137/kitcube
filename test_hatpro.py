#!/usr/bin/env python

import python.adeitools as adei
from python.hatpro import read_server_config, read_sensor_config

config_server = './config/server.ini'
config_sensor = './config/hatpro.ini'
servername = 'HEADS'
sensorname = 'L2A.ATM.WAT.VAP.CNT'

def test_config():

    host, server = read_server_config(config_server, servername)
    assert host != '' and server != ''

    group = read_sensor_config(config_sensor, sensorname)
    assert group == 'Data_080_RPG_L2A'


def test_adei_init():

    host, server = read_server_config(config_server, servername)
    adei.adeiReader()
    assert 1





