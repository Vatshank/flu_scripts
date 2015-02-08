import numpy as np
import networkx as nx
impo
    #G = nx.scale_free_graph(N)
    
    matching[k] = len(nx.max_weight_matching(G))
    
    nd = (N-matching[k])/N
    
    test[k] = nd
    
    
plt.figure()
plt.plot(test)

            
plt.figure()
plt.plot(matching)
plt.show()    