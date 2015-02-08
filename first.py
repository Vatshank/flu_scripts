import os
import datetime
import pickle
import numpy as np
import matplotlib.pyplot as plt

count = 0

with open('Data/h3n2_1950_2005.fasta','r') as f:
    line = f.readline()
    count+=1

    
    while line!='': #while count<2000:
        print count  
        if line[0] == '>':
            print "New strain begins"
            if "|Name" in line:
                year = str(line.split('|Name')[0][-2:])
                strain_id = line.split(":")[1]
            
                if os.path.isdir('out/'+year) is not True:
                    try:
                        os.mkdir('out/'+year)
                    except:
                        print "Surprise Motherfucker! Cannot make directory."
                
                with open ("out/"+year+"/"+strain_id+".fasta","w") as f_strain:
                    f_strain.write(line)
                    line = f.readline()                    
                    count+=1
                    while line[0] != ">" or line[0]!="":
                        f_strain.write(line)
                        line = f.readline()        
                        count+=1            
            else:
                line= f.readline()
                count+=1
        else:
            line= f.readline()
            count+=1