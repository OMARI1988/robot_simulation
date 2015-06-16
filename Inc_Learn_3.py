import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
from data_processing import *
import operator

P = process_data()

for scene in range(1,20):
    P._read(scene)                                  #Objects, Graph, Sentences
    P._fix_sentences()                              #remove sapces and dots
    P._more_fix_sentences()                              #remove sapces and dots
    P._print_scentenses()
    P._fix_data()       # correction to Data removing 20 and 40
    P._compute_features_for_all()
    P._compute_features_for_moving_object()
    P._transition()         
    P._grouping()
    P._compute_unique_color_shape()
    P._compute_unique_dist_dir()
    P._compute_unique_motion()
       
    P._get_all_words()
    P._build_phrases()
    #P._build_vector_hyp()              #similar to grammer
    #P._build_hyp1()              #vision
    P._build_hyp2()              #similar to grammer
    P._test_action_hyp()
    print '**================= end of scene ===================**'
    
#print P.all_words
#print len(P.all_words)
    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
