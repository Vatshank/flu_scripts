import os
import pickle

count = 0

with open('Data/h3n2_1950_2012.fasta','r') as f:
    line = f.readline()
    count+=1        

    while line!='': #while count<1000:
        print count 
        if line[0] == '>':
            
            print "New strain begins"
            if "|Name" in line:
                year = str(line.split('|Name')[0][-2:])
                strain_id = line.split(":")[1]
                segment = line.split("|")[-4].split(":")[-1]
                start = int(line.split(":")[2].split("|")[0].split("-")[0])
                stop = int(line.split(":")[2].split("|")[0].split("-")[1])
                length = stop - start +1
                
                if segment[0]!="H" and segment[0]!="N" and segment[0]!="h" and segment[0]!="n":
                    print "Unacceptable segment value"
                    break
                                
                if os.path.isdir('Out1/'+year) is not True:
                    try:
                        os.mkdir('Out1/'+year), os.mkdir("Out1/"+year+"/HA"), os.mkdir("Out1/"+year+"/NA")
                    except:
                        print "Cannot make directory."
                
                if segment[0]=="H" or segment[0]=="h":
                    ## Removing HA sequences with lengths other than 1701 bp 
                    if (length == 1701):
                
                        with open ("Out1/"+year+"/HA/"+strain_id+".fasta","w") as f_strain:
                            f_strain.write(line)
                            line = f.readline()                    
                            count+=1
                            
                            while line[0] != ">" :
                                f_strain.write(line)
                                line = f.readline()
                                if line == "":
                                    break        
                                count+=1
                    else:
                        line= f.readline()
                        count+=1
                                
                else:
                    ## Removing NA sequences with lengths other than 1410 bp
                    if (length == 1410):
                    
                        with open ("Out1/"+year+"/NA/"+strain_id+".fasta","w") as f_strain:
                            f_strain.write(line)
                            line = f.readline()                    
                            count+=1
                            
                            while line[0] != ">":
                                f_strain.write(line)
                                line = f.readline()
                                if line == "":
                                    break                
                                count+=1
                    else:
                        line= f.readline()
                        count+=1
                                                        
            else:
                line= f.readline()
                count+=1
        else:
            line= f.readline()
            count+=1