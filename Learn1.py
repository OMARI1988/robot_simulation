import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
dir1 = '/home/omari/Datasets/robot/motion/scene'

for scene in range(1,30):
    G=nx.Graph()
    print 'reading scene number:',scene
    f = open(dir1+str(scene)+'.txt', 'r')
    data = f.read().split('\n')
    sentences = []
    objects = []
    gripper = []
    for count,line in enumerate(data):
        if line.split(':')[0] == 'sentence':    sentences.append(count+1)
        if line.split(':')[0] == 'object' and line.split(':')[1]!='gripper':    objects.append(count+1)
        if line.split(':')[0] == 'object' and line.split(':')[1]=='gripper':    gripper.append(count+1)
            
    S = {}
    for count,s in enumerate(sentences):
        if data[s].split(':')[0] == 'GOOD': S[count] = data[s].split(':')[1]
        
    O = {}
    for count,o in enumerate(objects):
        G.add_node(count)
        O[count] = {}
        O[count][data[o].split(':')[0]] = np.asarray(map(float,data[o].split(':')[1].split(',')[:-1]))          #x
        O[count][data[o+1].split(':')[0]] = np.asarray(map(float,data[o+1].split(':')[1].split(',')[:-1]))      #y
        O[count][data[o+2].split(':')[0]] = np.asarray(map(float,data[o+2].split(':')[1].split(',')[:-1]))      #z
        O[count][data[o+3].split(':')[0]] = np.asarray(map(float,data[o+3].split(':')[1].split(',')))           #color
        O[count][data[o+4].split(':')[0]] = float(data[o+4].split(':')[1])                                      #shape
            
    for o in gripper:
        G.add_node('G')
        O['G'] = {}
        O['G'][data[o].split(':')[0]] = np.asarray(map(float,data[o].split(':')[1].split(',')[:-1]))      #x
        O['G'][data[o+1].split(':')[0]] = np.asarray(map(float,data[o+1].split(':')[1].split(',')[:-1]))  #y
        O['G'][data[o+2].split(':')[0]] = np.asarray(map(float,data[o+2].split(':')[1].split(',')[:-1]))  #z
        
    # comuting motion
    for i in O:
        dx = (O[i]['x'][:-1]-O[i]['x'][1:])**2
        dy = (O[i]['y'][:-1]-O[i]['y'][1:])**2
        dz = (O[i]['z'][:-1]-O[i]['z'][1:])**2
        O[i]['speed'] = np.round(np.sqrt(dx+dy+dz)*100)
        O[i]['speed'][O[i]['speed']!=0] = 1
        
    # removing frames were agent is static
    ind = np.where(O['G']['speed']==0)[0]
    for i in O:
        O[i]['speed'] = np.delete(O[i]['speed'],ind)
        
    # compute relative motion
    R = {}
    r_speed = []
    keys = O.keys()
    for i in range(len(keys)-1):
        for j in range(i+1,len(keys)):
            k1 = keys[i]
            k2 = keys[j]
            for s in np.abs(O[k1]['speed'] - O[k2]['speed']):
                if r_speed == []: r_speed = [s]
                else : r_speed = np.vstack([r_speed,s])
                
                
    # cluster relative motion
    est = KMeans(n_clusters=2)
    est.fit(r_speed)
    for i in range(len(keys)-1):
        for j in range(i+1,len(keys)):
            r = []
            k1 = keys[i]
            k2 = keys[j]
            for s in np.abs(O[k1]['speed'] - O[k2]['speed']):
                if r == []: r = [s]
                else : r = np.vstack([r,s])
            R[(k1,k2)] = est.predict(r)
            
    # comput the transition intervals
    frames = len(r)
    n = np.sum(range(len(keys)))
    r = np.zeros((n,frames),dtype=np.int8)
    counter = 0
    for i in range(len(keys)-1):
        for j in range(i+1,len(keys)):
            k1 = keys[i]
            k2 = keys[j]
            r[counter,:] = R[(k1,k2)]
            counter += 1
    col = r[:,0]
    transition = [0]
    for i in range(1,frames):
        if np.sum(np.abs(col-r[:,i]))!=0:
            col = r[:,i]
            transition.append(i)
                
    # plot the different graphs
    for T in transition:
        for i in range(len(keys)-1):
            for j in range(i+1,len(keys)):
                G.add_edge(k1,k2,speed=0)
        nx.draw(G)  # networkx draw()
        #plt.savefig("node_colormap.png") # save as png
        plt.show() # display
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
