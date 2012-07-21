#! /usr/bin/env python
import sys, threading

from scapy.all import *
from functions import *
from queue_process import *

# from optparse import OptionParser
# https://github.com/pentestmonkey/gateway-finder/blob/master/gateway-finder.py


if len(sys.argv) == 1:
    print 'Error, no arguments'
    print 'Usage: %s <pcap file|dev>' % sys.argv[0]
    sys.exit(1)
    

src = sys.argv[1]

# Get the interfaces list
devs = getinterfaces()

if devs.__contains__(src):
    isdev = True    
else:
    isdev = False

if isdev:
    print '[-]\tSniffing...'
    try:
        sniff(store=0, prn=lambda x:processpkt(x), iface=src, count=10000)
    except KeyboardInterrupt:
        print '[+]\tStopped sniffing!'
else:
    print '[-]\tReading file %s' % str(src)
    try:    
        sniff(store=0, prn=lambda x:processpkt(x), offline=src, count=10000)
        print '[+]\tFinished reading file %s!' % str(src)
    except KeyboardInterrupt:
        print '[+]\tUser stopped reading file!'

# Process queues
qthread = threading.Thread(target=processQs)

qthread.setDaemon(True)
qthread.start()

# Wait for processing thread to complete all tasks in queue
Ether_comms_Q.join()

createmap()