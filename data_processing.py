import numpy as np
import networkx as nx
dir1 = '/home/omari/Datasets/robot/motion/scene'

def read(scene):
    print 'reading scene number:',scene
    f = open(dir1+str(scene)+'.txt', 'r')
    data = f.read().split('\n')
    G = nx.Graph()
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
    return O,G,S
    
    
    
