import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import sys


def pareto_sequence(n,k,alpha): 
    ##Calculate x_m, parameter of the pareto distribution## 
    x_m = k*(alpha-1)/alpha
    
    ##Generate random numbers following the pareto powerlaw distribution##
    return [int(x_m/(random.random()**(1.0/alpha))) for i in range(n)]


#sys.setrecursionlimit(10000)

#plt.close('all')
N_ITER = 2
N = 300
nbins = 30

avg_degree = np.zeros(nbins)
test = np.zeros(nbins)
matching = np.zeros(nbins)

alpha_set = [1.2, 1.4, 1.8, 2.0] ##Correspond to gamma = [2.2, 2.4, 2.8]; alpha = gamma + 1##

plt.figure()

for alpha in alpha_set:
    
    for i in range(N_ITER):
        print i
    
        for k in range (nbins):
            
            ##Get the degree sequence##
            degree_seq = pareto_sequence(N, k, alpha)
            
            #if (sum(degree_seq)%2!=0):
            #    degree_seq[0]+=1
            
            G = nx.directed_configuration_model(degree_seq, degree_seq)
            
            ##Construct equivalent bipartite graph##
            bi = nx.Graph()
            
            bi.add_nodes_from(G.nodes(), bipartite = 0)
            bi.add_nodes_from([x+N for x in G.nodes()],bipartite = 1)
            bi.add_edges_from([(x[0],x[1]+N) for x in G.edges()])
            
            #try:
            matching[k] = len(nx.max_weight_matching(bi))/2.0
            #
            #except AssertionError:
            #    continue
            
            #print k
           	
           	##Fraction of driver nodes##
            nd = (N-matching[k])/N
            test[k] += nd

    ##Plotting##
    test/=N_ITER
    x =np.linspace(0,30, num = 30)    
    plt.yscale('log')
    plt.plot(test,linestyle='', marker = 'o', label = "alpha = "+str(alpha)+" Min input theorem")          
    plt.plot(np.exp(-1/2*(1-(1.0/(alpha)))*x), label = "alpha = "+str(alpha)+" Cavity method")
    

plt.xlabel('<k>')
plt.ylabel('nD')
plt.legend()
plt.show()      