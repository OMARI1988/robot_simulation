import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
from data_processing import *
dir1 = '/home/omari/Datasets/robot/motion/scene'

hyp = {}
for scene in range(1,120):
    O,G,S = read(scene)     #Objects, Graph, Sentences
    
    # initial parameter
    frames = len(O['G']['x'])-1     # we remove the first one to compute speed
    keys = O.keys()
    n = np.sum(range(len(keys)))
    
    # correction to Data removing 20 and 40
    for i in O:
        O[i]['x'] = np.delete(O[i]['x'],[20,40])
        O[i]['y'] = np.delete(O[i]['y'],[20,40])
        O[i]['z'] = np.delete(O[i]['z'],[20,40])
        
    # finding the moving object ! fix this
    o_mov = []
    for i in O:
        if i != 'G':
            x = np.abs(O[i]['x'][0]-O[i]['x'][-1])
            y = np.abs(O[i]['y'][0]-O[i]['y'][-1])
            z = np.abs(O[i]['z'][0]-O[i]['z'][-1])
            if (x+y+z) > 0:
                o_mov = i
                
    c = O[o_mov]['color']
    color = (c[0],c[1],c[2])
    shape = O[o_mov]['shape']
    
    colors = []
    shapes = []
    for i in O:
        if i != 'G':
            c = O[i]['color']
            C = (c[0],c[1],c[2])
            s = O[i]['shape']
            if C not in colors: colors.append(C)
            if s not in shapes: shapes.append(s)
            
    
    for i in S:
        # unique words
        words = []
        w = S[i].split(' ')
        for word in w:
            if word not in words: words.append(word)
        #update hypothesis
        for word in words:
            if word not in hyp:
                hyp[word] = {}
                hyp[word]['shape'] = {}
                hyp[word]['color'] = {}
                hyp[word]['counter'] = 0
                
            for shape in shapes:
                if shape not in hyp[word]['shape']:
                    hyp[word]['shape'][shape] = 0
                    
            for color in colors:    
                if color not in hyp[word]['color']:
                    hyp[word]['color'][color] = 0
                
            for color in colors:    
                hyp[word]['color'][color] += 1
                
            for shape in shapes:
                hyp[word]['shape'][shape] += 1
                
            hyp[word]['counter'] += 1

    if scene >= 110:
        print hyp['blue']
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
