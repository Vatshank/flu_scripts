import random
import glob
import os

YearList = os.listdir("C:/Users/Vatshank/Desktop/Population Genetics/flu/Out1/")

for year in YearList:
    HASequences = glob.glob("Out1/"+year+"/HA/*")
    NASequences = glob.glob("Out1/"+year+"/NA/*")
    
    NoHASequences = len(HASequences)
    NoNASequences = len(NASequences)
    
    #print year, NoHASequences, NoNASequences
    
    if (NoHASequences > 20):
        SampleSizeHA = 20
    else:
        SampleSizeHA = NoHASequences
        
    if (NoNASequences > 20):
        SampleSizeNA = 20
    else:
        SampleSizeNA = NoNASequences     
     
    RandomSampleHA = random.sample(range(0,NoHASequences), SampleSizeHA)
    RandomSampleNA = random.sample(range(0,NoNASequences), SampleSizeNA)
    
    for SampleNo in RandomSampleHA:
        print HASequences[SampleNo]
        with open("Out1/tree_sequences/tree_sequences_HA_1.fasta","a") as f_out_HA:
            with open(HASequences[SampleNo],"r") as f_in:
                line = f_in.readline()
                while line!="":
                    f_out_HA.write(line)
                    line = f_in.readline()
    
    for SampleNo in RandomSampleNA:
        print NASequences[SampleNo]
        with open("Out1/tree_sequences/tree_sequences_NA_1.fasta","a") as f_out_NA:
            with open(NASequences[SampleNo],"r") as f_in:
                line = f_in.readline()
                while line!="":
                    f_out_NA.write(line)
                    line = f_in.readline()
                     
   