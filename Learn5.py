import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
from data_processing import *
dir1 = '/home/omari/Datasets/robot/motion/scene'

hyp = {}
for scene in range(1,2):
    O,G,S = read(scene)     #Objects, Graph, Sentences
    
    # correction to Data removing 20 and 40
    #for i in O:
    #    O[i]['x'] = np.delete(O[i]['x'],[20,40])
    #    O[i]['y'] = np.delete(O[i]['y'],[20,40])
    #    O[i]['z'] = np.delete(O[i]['z'],[20,40])
    
    # initial parameter
    frames = len(O['G']['x'])     # we remove the first one to compute speed
    keys = O.keys()
    #n = np.sum(range(len(keys)))
    n = len(keys)-1
        
    # finding the moving object ! fix this
    o_mov = []
    for i in O:
        if i != 'G':
            x = np.abs(O[i]['x'][0]-O[i]['x'][-1])
            y = np.abs(O[i]['y'][0]-O[i]['y'][-1])
            z = np.abs(O[i]['z'][0]-O[i]['z'][-1])
            if (x+y+z) > 0:
                o_mov = i
                
    # computing distance
    dis = np.zeros((n,frames),dtype=np.int8)
    counter = 0
    for i in range(len(keys)):
        k2 = keys[i]
        if k2 != o_mov and k2 != 'G':
            dx = np.abs(O[o_mov]['x'][:]-O[k2]['x'][:])
            dy = np.abs(O[o_mov]['y'][:]-O[k2]['y'][:])
            dz = np.abs(O[o_mov]['z'][:]-O[k2]['z'][:])
            A = dx+dy+dz
            A[A<=1] = 1
            A[A>1] = 0
            dis[counter,:] = A
            counter += 1
            
    # computing direction
    dirx = np.zeros((n,frames),dtype=np.int8)
    diry = np.zeros((n,frames),dtype=np.int8)
    dirz = np.zeros((n,frames),dtype=np.int8)
    counter = 0
    for i in range(len(keys)):
        k2 = keys[i]
        if k2 != o_mov and k2 != 'G':
            dx = O[o_mov]['x'][:]-O[k2]['x'][:]
            dy = O[o_mov]['y'][:]-O[k2]['y'][:]
            dz = O[o_mov]['z'][:]-O[k2]['z'][:]
            dirx[counter,:] = np.sign(dx).astype(int)
            diry[counter,:] = np.sign(dy).astype(int)
            dirz[counter,:] = np.sign(dz).astype(int)
            counter += 1
    
    # finding locations
    loci = {}
    locf = {}
    for key in keys:
        if key != 'G':
            loci[key] = [O[key]['x'][0],O[key]['y'][0]]
            locf[key] = [O[key]['x'][-1],O[key]['y'][-1]]
        
    # plotting the initial and final scene
    f, ax = plt.subplots(2) # first initial , second final
    for sub in range(2):
    
        if sub == 0:        #initial
            loc = loci
        else:
            loc = locf
    
        # Creating the graph structure
        G = nx.Graph()
        for key in keys:
            if key != 'G':
                G.add_node(str(key))
                G.add_node('of_c'+str(key));         #color
                G.add_node('of_s'+str(key));         #shape
                G.add_node('of_l'+str(key));         #location
                G.add_edge(str(key),'of_c'+str(key),value=O[key]['color'])
                G.add_edge(str(key),'of_s'+str(key),value=O[key]['shape'])
                G.add_edge(str(key),'of_l'+str(key),value=loc[key])
    
        plt.sca(ax[sub])
        
        # layout graphs with positions using graphviz neato
        pos=nx.graphviz_layout(G,prog="neato")
        # color nodes the same in each connected subgraph
        C=nx.connected_component_subgraphs(G)
        cK = 0
        for i in C:
            cK += 1
        C=nx.connected_component_subgraphs(G)
        colors = np.linspace(.2,.6,cK)
        for count,g in enumerate(C):
            #c=[random.random()]*nx.number_of_nodes(g) # random color...
            c=[colors[count]]*nx.number_of_nodes(g) # same color...
            nx.draw(g,
                 pos,
                 node_size=80,
                 node_color=c,
                 vmin=0.0,
                 vmax=1.0,
                 with_labels=False
                 )
        #nx.draw(G)  # networkx draw()
        ax[sub].axis('on')
        plt.tick_params(axis='x',which='both',bottom='off',top='off',labelbottom='off')
        plt.tick_params(axis='y',which='both',right='off',left='off',labelleft='off')
        #plt.savefig("node_colormap.png") # save as png
    plt.show() # display

    
    
    
    
    
    
    
    
    
    
    
    
