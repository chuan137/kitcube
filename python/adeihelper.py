import re
import sys
import datetime
import calendar
import colorstring
import base64
import csv
import xml.etree.ElementTree as ET
import traceback
import urllib2 as urllib

ADEI_Time_Format = '%d-%b-%y %H:%M:%S.%f'

def xmlparser(handler):
    tree = ET.parse(handler)
    result = []
    for child in tree.getroot():
        result.append(child.attrib)
    return result

def csvparser(handler):
    rows = csv.reader(handler, skipinitialspace=True)
    fields = rows.next()
    data = [row for row in rows if row]
    return zip(fields, *data)

def print_exc():
    exctype, value, tb  = sys.exc_info()
    filename, linenumber, functionname, text =  traceback.extract_tb(tb, 1)[0]
    sys.stderr.write("[Error] Unexpected exception\n")
    sys.stderr.write("            type: %s\n" % exctype)
    sys.stderr.write("         message: %s\n" % colorstring.ERROR(value.message))
    sys.stderr.write("        function: %s\n" % colorstring.ERROR(functionname))
    sys.stderr.write("            text: %s\n" % text)
    sys.stderr.write("            file: %s: %s\n" % (filename, linenumber))

def adei_timestamp(adeitimestr):
    timestamp = datetime.datetime.strptime(adeitimestr, ADEI_Time_Format)
    timestamp = calendar.timegm(timestamp.timetuple())
    return timestamp

def query_csv(url, username=None, password=None):
    request = urllib.Request(url)
    if username and password:
        base64string = base64.encodestring('%s:%s' % ( username, password ) )
        request.add_header("Authorization", "Basic %s" % base64string)
    fp = urllib.urlopen(request)
    resp = csvparser(fp)
    return resp

def query_xml(url, username=None, password=None):
    request = urllib.Request(url)
    if username and password:
        base64string = base64.encodestring('%s:%s' % ( username, password ) )
        request.add_header("Authorization", "Basic %s" % base64string)
    fp = urllib.urlopen(request)
    return xmlparser(fp)
 
