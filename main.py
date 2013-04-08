#! /usr/bin/env python
import sys, threading
sys.dont_write_bytecode = True

from scapy.all import *
from functions import *
from queue_process import *

def main(arg):

    # from optparse import OptionParser
    # https://github.com/pentestmonkey/gateway-finder/blob/master/gateway-finder.py
    
    if len(arg) == 1:
        print 'Error, no arguments'
        print 'Usage: %s <pcap file|dev>' % arg[0]
        sys.exit(1)

    src = arg[1]
    
    # Process queues
    qthread = threading.Thread(target=processQ)
    qthread.setDaemon(True)
    qthread.start()
    
    # Get the interfaces list
    devs = getinterfaces()
    
    if devs.__contains__(src):
        isdev = True    
    else:
        isdev = False
    
    if isdev:
        print '[-]\tSniffing...'
        try:
            sniff(store=0, prn=lambda x:processpkt(x), iface=src)
        except KeyboardInterrupt:
            print '[+]\tStopped sniffing!'
    else:
        print '[-]\tReading file %s' % str(src)
        try:    
            sniff(store=0, prn=lambda x:processpkt(x), offline=src, count=10000)
            print '[+]\tFinished reading file %s!' % str(src)
        except KeyboardInterrupt:
            print '[+]\tUser stopped reading file!'
    
    # Notify sniffing has ended
    processpkt(None)
    
    # Wait for processing thread to complete all tasks in queue
    qthread.join()

    
if __name__ == "__main__":
    main(sys.argv)
else:
    print '\nPlease run me as "main", thanks :)'