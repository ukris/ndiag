from scapy.all import *
from functions import *

# Track nodes
Ether_nodes    = []
IP_nodes       = []
# 
Ether_comms    = []

Ether2IP_join  = []

def processQ():

    loop = True

    while loop:

        pkt = pkt_Q.get(True)

        if pkt == None:
            loop = False
            break
        
        # Set defaults
        Ether_src = None
        Ether_dst = None
        IP_src    = None
        IP_dst    = None

        # Get the layers
        Ether_layer  = pkt.getlayer(Ether)
        IP_layer     = pkt.getlayer(IP)

        # Get addresses and do mapping before fancy stuff ------------------

        # Ether layer   
        Ether_src = Ether_layer.src.replace(':', '-')
        Ether_dst = Ether_layer.dst.replace(':', '-')
        
        # IP layer, may not have IP layer (e.g. ARP)
        if not IP_layer == None:
            IP_src = IP_layer.src
            IP_dst = IP_layer.dst
            
            print Ether_src + ' ' + Ether_dst + ' ' + IP_src + ' ' + IP_dst
        
        pkt_Q.task_done()


def net_roles():

    remNode = []

    for n in G.nodes_iter():
        if G.node[n]['nodeType'] == 'Ether':
            IPnodes = []
            for n_nei in G.neighbors_iter(n):
                if G.node[n_nei]['nodeType'] == 'IP':
                    IPnodes.append((n, n_nei))
            if len(IPnodes) == 1:
                remNode.append(IPnodes[0])
            IPnodes = []
        
    for n, n_nei in remNode:
        addr = G.node[n_nei]['text']
        G.remove_node(n_nei)
        G.node[n]['nodeType'] = 'combi'
        G.node[n]['ether'] = G.node[n]['text']
        G.node[n]['IP'] = addr
        G.node[n]['text'] += '\n' + addr


# Check whether you already have the value in the list
def addNode(typ, element, node_List):

    if typ == 'Ether_edge':
        if element not in node_List:
            node_List.append(element)
            G.add_edge(*element) #      * = unpack truple inline
        return

    if typ == 'Ether2IP_edge':
        if element not in node_List:
            node_List.append(element)
            G.add_edge(*element) #      * = unpack truple inline
        return

    i = 0
    name = None

    if element not in node_List:
        node_List.append(element)
        
        i = node_List.index(element)
        name = typ + '_' + str(i)
        G.add_node(name, nodeType=typ, text=element)

	print '[+] Added ' + element
        
    else:
        i = node_List.index(element)
        name = typ + '_' + str(i)
    
    return name
