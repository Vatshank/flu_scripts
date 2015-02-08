##NOTE: Powerlaw function is used here with an exponential cutoff
import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt

##Approximate values for c(gamma,kappa)
def gen_c_gamma(gamma,kappa):
    n=1000 ##Number of terms in the approximation
    sum_temp = 0
    for k in range(1,n+1):
        sum_temp+=(k**(-1.0*gamma)*np.exp(-1.0*k/kappa))
        ##print k, sum
    return (1/sum_temp)

##Average degree for given (gamma,kappa)        
def expected_degree(n,gamma,kappa):
    return (gen_c_gamma(gamma,kappa)/gen_c_gamma(gamma-1,kappa))
           
##CDF values for the powerlaw
def gen_CDF_powerlaw(n,gamma,kappa):
    sum_temp = 0
    c = gen_c_gamma(gamma,kappa)
    arr_CDF = np.zeros(n+1)
    arr_CDF[0] = 0 ##Setting the first(zero) index of the array to zero
    for k in range(1,n+1):
        ##print sum_temp
        sum_temp+=c*(k**(-1.0*gamma))*np.exp(-1.0*k/kappa)
        arr_CDF[k] = sum_temp
        
    return arr_CDF

##Get the random numbers from the powerlaw using the CDF function above
def gen_rand_powerlaw(n, gamma, kappa):
    ##arr_powerlaw = np.zeros(n)
    arr_powerlaw = []
    arr_uni = [random.random() for i in range(n)]
    arr_CDF = gen_CDF_powerlaw(n,gamma,kappa)
    for i in range(n):
        temp = arr_uni[i]
        for j in range(n):
            if (temp>=arr_CDF[j] and temp<=arr_CDF[j+1]):
                arr_powerlaw.append(j+1)
                ##print j+1
                break
    
    return arr_powerlaw

##Plot variation in <k> as a function of kappa
#k_avg = np.zeros(100000)
#for kappa in range(1,100000):
#    k_avg[kappa] = expected_degree(100, 2.0, kappa)        
#
#plt.figure()
#plt.plot(k_avg)

#####################
#####################
nbins = 30
avg_degree = np.zeros(nbins)
test = np.zeros(nbins)
matching = np.zeros(nbins)
plt.figure()
degree_seq = []

N_ITER = 10
N = 500
kappa_set = [float('inf')]

for kappa in kappa_set:
    
    for i in range(N_ITER):
        print i
        
        arr_gamma = np.linspace(0,5,30)
        for k in range (nbins):
            
            ##Get the degree sequence##
            degree_seq = gen_rand_powerlaw(N,arr_gamma[k], kappa)
            
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
    plt.plot()
    plt.plot(arr_gamma,test,label = kappa)    

#x =np.linspace(0,30, num = 30)    
#plt.yscale('log')
#plt.plot(test,linestyle='', marker = 'o', label = "alpha = "+str(alpha)+" Min input theorem")          
#plt.plot(np.exp(-1/2*(1-(1.0/(alpha)))*x), label = "alpha = "+str(alpha)+" Cavity method")
#    
#
#plt.xlabel('<k>')
#plt.ylabel('nD')
#plt.legend()
plt.show()              
