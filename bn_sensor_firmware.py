import network
import urllib2
global con_status

def con_check():
    try:
        urllib2.urlopen('http://192.168.86.1', timeout=1)
        return True
    except urllib2.URLError as err:
        return False


