import sys
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from Bio import SeqIO
from Bio.Alphabet import generic_dna, generic_protein
from Bio.SeqRecord import SeqRecord
from Bio.Align import MultipleSeqAlignment
import random


sys.path.append("C:/Python27/Lib/site-packages/")

YearList = os.listdir("C:/Users/Vatshank/Desktop/Population Genetics/flu/Out1/")
  
lengthHA = 1701 ##Length of the nucleotide sequence
lengthNA = 1410


NoOfSamples = 50

Segments = ["HA", "NA"]

mutSynHA = np.zeros(lengthHA/3)
mutSynNA = np.zeros(lengthNA/3)

mutNonsynHA = np.zeros(lengthHA/3)
mutNonsynNA = np.zeros(lengthNA/3)

for year in YearList:
    HASequences = glob.glob("Out1/"+year+"/HA/*")
    NASequences = glob.glob("Out1/"+year+"/NA/*")
    
    NoHASequences = len(HASequences)
    NoNASequences = len(NASequences)
    
    if (NoHASequences > 20):
        SampleSizeHA = 20
    else:
        SampleSizeHA = NoHASequences
        
    if (NoNASequences > 20):
        SampleSizeNA = 20
    else:
        SampleSizeNA = NoNASequences 
    
    #SampleSizeHA = NoHASequences
    #SampleSizeNA = NoNASequences    
    
    RandomSampleHA = random.sample(range(0,NoHASequences), SampleSizeHA)
    RandomSampleNA = random.sample(range(0,NoNASequences), SampleSizeNA)
    
    NucleoSequencesHA = []
    NucleoSequencesNA = []
    
    ProteinSequencesHA = []
    ProteinSequencesNA = []
        
    for SampleNo in RandomSampleHA:
        NucleoSequencesHA.append(SeqIO.read(HASequences[SampleNo],"fasta"))
        ProteinSequencesHA.append(SeqRecord(SeqIO.read(HASequences[SampleNo],"fasta").seq.translate(), id = SeqIO.read(HASequences[SampleNo],"fasta").id))
    
    for SampleNo in RandomSampleNA:
        NucleoSequencesNA.append(SeqIO.read(NASequences[SampleNo],"fasta"))
        ProteinSequencesNA.append(SeqRecord(SeqIO.read(NASequences[SampleNo],"fasta").seq.translate(), id = SeqIO.read(NASequences[SampleNo],"fasta").id))
    
    NucleoAlignmentHA = MultipleSeqAlignment(NucleoSequencesHA)
    NucleoAlignmentNA = MultipleSeqAlignment(NucleoSequencesNA)
    
    ProteinAlignmentHA = MultipleSeqAlignment(ProteinSequencesHA)
    ProteinAlignmentNA = MultipleSeqAlignment(ProteinSequencesNA)       
    
    codonsHA=[]
    codonsNA=[]
        
    for codon in range(NucleoAlignmentHA.get_alignment_length()/3):                        ## getting codons from the transcript
        
        codonsHA.append(map(str,[X.seq for X in NucleoAlignmentHA[:,(3*codon):(codon+1)*3]]))
        
    for codon in range(NucleoAlignmentNA.get_alignment_length()/3):                        ## getting codons from the transcript
        
        codonsNA.append(map(str,[X.seq for X in NucleoAlignmentNA[:,(3*codon):(codon+1)*3]]))

    codonsHA = (np.array(codonsHA).T)    
    codonsNA = (np.array(codonsNA).T)
    MatrixCodonsHA = codonsHA                               ## using transpose of the matrix
    MatrixCodonsNA = codonsNA
    
    MatrixProteinHA  = np.array(ProteinAlignmentHA)
    MatrixProteinNA  = np.array(ProteinAlignmentNA)
    
    print MatrixCodonsHA.shape, MatrixProteinHA.shape, MatrixCodonsNA.shape, MatrixProteinNA.shape
    
    UniCodonsHA = []
    UniProteinHA = []
    
    UniCodonsNA = []
    UniProteinNA = []
    
    for n in range(MatrixCodonsHA.shape[1]):                            ## getting uni, which has the number of different types codons at each site
        UniCodonsHA.append(np.unique(MatrixCodonsHA[:,n]).shape[0])	        
        
    for n in range(MatrixProteinHA.shape[1]):
        UniProteinHA.append(np.unique(MatrixProteinHA[:,n]).shape[0])
    
    for n in range(MatrixCodonsNA.shape[1]):                            ## getting uni, which has the number of different types codons at each site
        UniCodonsNA.append(np.unique(MatrixCodonsNA[:,n]).shape[0])	        
        
    for n in range(MatrixProteinNA.shape[1]):
        UniProteinNA.append(np.unique(MatrixProteinNA[:,n]).shape[0])    
                
    ArrUniCodonsHA = np.array(UniCodonsHA)>1                                ## same as->  arr_uni[arr_uni==1] = 0 #arr_uni[arr_uni>1] = 1  
    ArrUniProteinHA  = np.array(UniProteinHA)>1    
    ArrUniCodonsNA = np.array(UniCodonsNA)>1                                ## same as->  arr_uni[arr_uni==1] = 0 #arr_uni[arr_uni>1] = 1  
    ArrUniProteinNA  = np.array(UniProteinNA)>1
                                                                                                                    
    ArrUniNonsynHA = ArrUniCodonsHA * ArrUniProteinHA
    ArrUniSynHA = ArrUniCodonsHA * (1-ArrUniProteinHA)
    ArrUniNonsynNA = ArrUniCodonsNA * ArrUniProteinNA
    ArrUniSynNA = ArrUniCodonsNA * (1-ArrUniProteinNA)
    
    mutSynHA+=ArrUniSynHA
    mutSynNA+=ArrUniSynNA

    mutNonsynHA+=ArrUniNonsynHA
    mutNonsynNA+=ArrUniNonsynNA


#mutSynHA=mutSynHA>1
#mutSynNA=mutSynNA>1
#
#mutNonsynHA=mutNonsynHA>1
#mutNonsynNA=mutNonsynNA>1