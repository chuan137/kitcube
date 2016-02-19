#!/usr/bin/env python
import sys
sys.path.insert(0, '../')

from python.adeireader import ADEIReader
from python.hatpro import read_server_config, read_sensor_config

config_server = '../config/server.ini'
config_sensor = '../config/hatpro.ini'
servername = 'HEADS'
sensorname = 'L2A.ATM.WAT.VAP.CNT'

def test_config():

    host, server, dbname = read_server_config(config_server, servername)
    assert host != '' and server != ''

    group, sensor_readable_name,_ = read_sensor_config(config_sensor, sensorname)
    assert group == 'Data_080_RPG_L2A'
    assert sensor_readable_name == 'atmosphere_water_vapor_content'


def test_adei_init():

    host, server,dbname = read_server_config(config_server, servername)
    adei = ADEIReader(host, server, dbname)

    adei_groups = adei.groups
    assert len(adei_groups) > 0

    g =  adei_groups[0]['db_group']
    adei.update_sensor_list(g)
    sensors = adei.sensors[g]
    assert len(sensors) > 0






