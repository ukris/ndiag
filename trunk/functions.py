# import me to main.py!
from scapy.all import *
import Queue

Ether_comms_Q = Queue.Queue(10000)

# Processing of packet to save to the queues
def processpkt(pkt):
    
    if pkt == None:
        Ether_comms_Q.put_nowait(pkt)
        return    
    
    if not pkt.name == 'Ethernet':
        return    
    
    try:
        Ether_comms_Q.put_nowait(pkt)
        
    except Queue.Full:
        
        print '*** TRAFFIC OVERLOAD ***\n*** Dropped packet... Sorry! ***'
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
