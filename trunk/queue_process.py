<<<<<<< .mine
from scapy.all import *
from functions import *

import networkx as nx
import matplotlib.pyplot as plt

Ether_nodes    = []
IP_nodes       = []

Ether_comms    = []

Ether2IP_join  = []

G = nx.DiGraph()

def processQs():

    while True:

        pkt = Ether_comms_Q.get(True)
        
        # Set defaults
        Ether_src_I = None
        Ether_dst_I = None
        IP_src_I    = None
        IP_dst_I    = None

        # Get the layers
        Ether_layer  = pkt.getlayer(Ether)
        IP_layer     = pkt.getlayer(IP)

        # Get addresses and do mapping before fancy stuff ------------------

        # Ether layer   
        Ether_src = Ether_layer.src.replace(':', '-')
        Ether_dst = Ether_layer.dst.replace(':', '-')
        
        Ether_src_I = addNode('Ether', Ether_src, Ether_nodes)
        Ether_dst_I = addNode('Ether', Ether_dst, Ether_nodes)
            
        # Set the Ether communications
        addNode('Ether_edge', (Ether_dst_I, Ether_src_I), Ether_comms)
        
        # IP layer, may not have IP layer (e.g. ARP)
        if not IP_layer == None:
            IP_src      = IP_layer.src
            IP_dst      = IP_layer.dst
            
            IP_src_I = addNode('IP', IP_src, IP_nodes)
            IP_dst_I = addNode('IP', IP_dst, IP_nodes)
            
            # Join Ether to IP
            addNode('Ether2IP_edge', (Ether_src_I, IP_src_I), Ether2IP_join)
            addNode('Ether2IP_edge', (Ether_dst_I, IP_dst_I), Ether2IP_join)

        # Do the fancy stuff -----------------------------------------------
        # Process relationships and assign network roles
        net_roles()
        
        Ether_comms_Q.task_done()


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
        
    else:
        i = node_List.index(element)
        name = typ + '_' + str(i)
    
    return name


def createmap():
    
    labels = dict((n,d['text']) for n,d in G.nodes(data=True))
    
    mapfile = 'map.png'    

    print '[-]\tCreating %s...' % mapfile
    
    nx.draw_graphviz(G, labels=labels, node_size=100, node_shape='o')    
#    nx.draw_graphviz(G, node_size=800)
    plt.savefig(mapfile)
    print '[+]\tWritten to %s!' % mapfile
    plt.show()

# http://stackoverflow.com/questions/3982819/networkx-node-attribute-drawing
# http://networkx.lanl.gov/reference/generated/networkx.drawing.nx_pylab.draw_networkx.html#networkx.drawing.nx_pylab.draw_networkx

# Lookup ion for interaction (updating the graph) also animate?
# http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.ion=======
from scapy.all import *
from functions import *

import networkx as nx
import matplotlib.pyplot as plt

Ether_nodes    = []
IP_nodes       = []

Ether_comms    = []

G = nx.DiGraph()

def processQs():

    while True:

        pkt = Ether_comms_Q.get(True)
        
        # Set defaults
        Ether_src_I = None
        Ether_dst_I = None
        IP_src_I    = None
        IP_dst_I    = None

        # Get the layers
        Ether_layer  = pkt.getlayer(Ether)
        IP_layer     = pkt.getlayer(IP)

        # Get addresses and do mapping before fancy stuff ------------------

        # Ether layer   
        Ether_src = Ether_layer.src.replace(':', '-')
        Ether_dst = Ether_layer.dst.replace(':', '-')
        
        Ether_src_I = addNode('Ether', Ether_src, Ether_nodes)
        Ether_dst_I = addNode('Ether', Ether_dst, Ether_nodes)
            
        # Set the Ether communications
        addNode('Ether_edge', (Ether_dst_I, Ether_src_I), Ether_comms)
        
        # IP layer, may not have IP layer (e.g. ARP)
        if not IP_layer == None:
            IP_src      = IP_layer.src
            IP_dst      = IP_layer.dst
            
            IP_src_I = addNode('IP', IP_src, IP_nodes)
            IP_dst_I = addNode('IP', IP_dst, IP_nodes)

            # Join Ether to IP
            G.add_edge(Ether_src_I, IP_src_I)
            G.add_edge(Ether_dst_I, IP_dst_I)

        # Do the fancy stuff -----------------------------------------------
        # Process relationships and assign network roles
        net_roles()
        
        Ether_comms_Q.task_done()


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
        print G.nodes(data=True)
        G.remove_node(n_nei)
        G.node[n]['nodeType'] = 'combi'
        G.node[n]['text'] += '\n' + addr

    print 20*'-'
        

# Check whether you already have the value in the list
def addNode(typ, element, node_List):

    if typ == 'Ether_edge':
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
        
    else:
        i = node_List.index(element)
        name = typ + '_' + str(i)
    
    return name


def createmap():
    
    labels = dict((n,d['text']) for n,d in G.nodes(data=True))
    
    mapfile = 'map.png'
    
    print '[-]\tCreating %s...' % mapfile
    nx.draw_graphviz(G, labels=labels, node_size=100)
#    nx.draw_graphviz(G, node_size=800)
    plt.savefig(mapfile)
    print '[+]\tWritten to %s!' % mapfile
    plt.show()

# http://stackoverflow.com/questions/3982819/networkx-node-attribute-drawing
# http://networkx.lanl.gov/reference/generated/networkx.drawing.nx_pylab.draw_networkx.html#networkx.drawing.nx_pylab.draw_networkx

# Lookup ion for interaction (updating the graph) also animate?
# http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.ion>>>>>>> .r5
