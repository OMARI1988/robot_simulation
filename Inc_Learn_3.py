import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
from data_processing import *
import operator

P = process_data()

for scene in range(1,2):
    P._read(scene)                                  # Objects, Graph, Sentences
    P._fix_sentences()                              # remove sapces and dots
    P._more_fix_sentences()                         # remove ? ! ( )
    P._print_scentenses()
    P._fix_data()                                   # correction to Data removing 20 and 40
    #P._compute_features_for_all()
    #P._compute_features_for_moving_object()
    #P._transition()         
    #P._grouping()                                   # generate the edges between the nodes that are the same in motion or touching
    P._compute_unique_color_shape()                 # P.colors, P.shapes
    ##P._compute_unique_dis()                       # not done yet !
    #P._compute_unique_dir_all()                     # P.directions_x,P.directions_y,P.directions_z, P.directions is for moving object and touching
    #P._compute_unique_motion()                      # P.total_motion = {1: {(0, 1): 1, (1, 0): 1}, 2: {(0, 1, 0): 1}}
    print P.colors,P.shapes
    
    
       
    P._get_all_words()                              # keep track of all the words that were ever mentioned
    print P.all_words
    P._build_phrases()                              # find the unique words in every valid sentence
    print P.words
    #P._build_vector_hyp()              #similar to grammer
    #P._build_hyp1()              #vision
    #P._build_hyp2()              #similar to grammer
    #P._test_action_hyp()
    print '**================= end of scene ===================**'
    
#print P.all_words
#print len(P.all_words)
    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
