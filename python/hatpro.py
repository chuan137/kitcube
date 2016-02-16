import ConfigParser


def read_server_config(configfile, servername):

    config = ConfigParser.ConfigParser()
    config.read(configfile)

    if config.has_section(servername):
        h = config.get(servername, 'DB_HOST')
        s = config.get(servername, 'DB_SERVER')
        db = config.get(servername, 'DB_NAME')
        return h, s, db


def read_sensor_config(configfile, sensorname):

    config = ConfigParser.ConfigParser()
    config.read(configfile)

    if config.has_section(sensorname):
        g = config.get(sensorname, 'group')
        m = config.get(sensorname, 'name')
        try:
            n = config.get(sensorname, 'axis2_length')
            n = int(n)
        except ConfigParser.NoOptionError:
            n = 1
        return g, m, n

def read_sensor_axis2(configfile, sensorname):

    config = ConfigParser.ConfigParser()
    config.read(configfile)

    if config.has_section(sensorname):
        u = config.get(sensorname, 'axis2_unit')
        v = config.get(sensorname, 'axis2_value')
        return u, map(float, v.split(','))


#
# def parseConfig(configfile, sensor_):
#     # read server and sensor info from configuration
#     # find sensor and group, then initialize adei server
#     # there should be only one matched sensor, check?
#
#     config = ConfigParser.ConfigParser()
#     config.read(deviceConfig)
#     config.read(serverConfig)
#
#     sensors = [dict(config._sections[a]) 
#             for a in config.sections() if re.match('^sensor\d+', a)]
#
#     servers = [dict(config._sections[a]) 
#             for a in config.sections() if re.match('^server', a)]
#
#     print sensors
#     try:
#         sensor = [s for s in sensors if s['id'] == sensor_ ]
#         sensor[0]
#     except IndexError:
#         print "sensor id %s is not found in configuration" % sensor_
#         sys.exit()
#     else:
#         print "sensor id %s found in configuration" % sensor_
#         sensor = sensor[0]
#
#     server = [ s for s in servers 
#             if s['__name__'] == sensor['server'] ]
#     group = sensor['group']
#
#     return (server[0], group)
#
#
# class adeiReader(adei.adeiReader):
#     def dostuff(self, group_, sensor_, date_):
#
#         # find stamp
#         stamp00 = self.groupLastStamp(group_)
#         stamp0 =  self.groupLastDayStamp(group_)
#         stampOptions = {
#                 '0d': stamp0, 
#                 '1d': stamp0 - 86400,
#                 '2d': stamp0 - 86400*2,
#                 '20d': stamp0 - 86400*20
#                 }
#         filestamp = stampOptions[date_]
#
#         # filenames 
#         filename = "./cache/%s.%s.%s.json" % (
#                 device_, sensor_, filestamp)
#
#         # update ? or not
#         update = 0
#         try:
#             with open(filename, 'r') as f:
#                 oldstamp = json.loads(f.read())['time'][-1]
#             if oldstamp > stamp0 and oldstamp < stamp00:
#                 update = 1
#             print 'update ? ', stamp0, oldstamp, stamp00, update
#         except:
#             if DEBUG_:
#                 # print filename
#                 adei.print_exc(filename)
#             update = 1
#
#         return (filestamp, update)
#
