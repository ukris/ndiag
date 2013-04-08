from scapy.all import *
import Queue

pkt_Q = Queue.Queue(10000)

# Processing of packet to save to the queues
def processpkt(pkt):
    
    if pkt == None:
        pkt_Q.put_nowait(pkt)
        print '[!]\tEnd of data'
        return    
    
    if not pkt.name == 'Ethernet':
        return    
    
    try:
        pkt_Q.put_nowait(pkt)
    except Queue.Full:
        print '*** TRAFFIC OVERLOAD ***'
        return        

# Gets a list of dev's (interfaces) - Rough, doesn't work for windows
def getinterfaces():

    devs = []
    f = open('/proc/net/dev','r')
    ifacelist = f.read().split('\n') 
    f.close()
    ifacelist.pop(0)
    ifacelist.pop(0)
    for line in ifacelist:
        ifacedata = line.replace(' ','').split(':')
        if (len(ifacedata) == 2) and (int(ifacedata[1]) > 0):
            devs.append(ifacedata[0])
    return devs