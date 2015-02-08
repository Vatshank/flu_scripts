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

def autocorrelation(arr, dmax):                                
    acorr = np.zeros(dmax)
    for d in range(1,min(dmax,arr.shape[0])):
        acorr[d]+=np.sum(arr[d:] * arr[:-d])
     
    return acorr
    
def crosscorrelation(arr_syn,arr_nonsyn,dmax):
    crosscorr = np.zeros(2*dmax)
    for d in range(1,min(dmax,arr_syn.shape[0])):
        crosscorr[d]+=np.sum(arr_syn[d:] * arr_nonsyn[:-d])
        crosscorr[d+dmax]+=np.sum(arr_nonsyn[d:] * arr_syn[:-d])
     
    return crosscorr
    
YearList = os.listdir("C:/Users/Vatshank/Desktop/Population Genetics/flu/Out1/")
  
nbins = 100
NoOfSamples = 50

density_syn_HA = []
density_nonsyn_HA = []

density_syn_NA = []
density_nonsyn_NA = []


Segments = ["HA", "NA"]

AcorrSynHA = np.zeros(nbins)
AcorrNonsynHA = np.zeros(nbins)
CrosscorrHA = np.zeros(2*nbins)                             
NormalizingVector = np.zeros(nbins)

AcorrSynNA = np.zeros(nbins)
AcorrNonsynNA = np.zeros(nbins)
CrosscorrNA = np.zeros(2*nbins)                             
NormalizingVector = np.zeros(nbins)
    
#for No in range(NoOfSamples):
#    print ">>>>>>>Sample No :" + str(No) 
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
    
    density_syn_HA.append(np.mean(ArrUniSynHA))
    density_nonsyn_HA.append(np.mean(ArrUniNonsynHA))

    density_syn_NA.append(np.mean(ArrUniSynNA))
    density_nonsyn_NA.append(np.mean(ArrUniNonsynNA))   
                
    AcorrSynHA+=autocorrelation(ArrUniSynHA, nbins)
    AcorrNonsynHA+=autocorrelation(ArrUniNonsynHA, nbins)
    CrosscorrHA+=crosscorrelation(ArrUniSynHA, ArrUniNonsynHA, nbins)                             
    NormalizingVector+=np.maximum(len(ArrUniNonsynHA)-np.arange(0,nbins), np.zeros(nbins))

    AcorrSynNA+=autocorrelation(ArrUniSynNA, nbins)
    AcorrNonsynNA+=autocorrelation(ArrUniNonsynNA, nbins)
    CrosscorrNA+=crosscorrelation(ArrUniSynNA, ArrUniNonsynNA, nbins)                             
    NormalizingVector+=np.maximum(len(ArrUniNonsynNA)-np.arange(0,nbins), np.zeros(nbins))    

AcorrSynHA/=NormalizingVector
AcorrNonsynHA/=NormalizingVector
CrosscorrHA[:nbins]/=NormalizingVector
CrosscorrHA[nbins:2*nbins]/=NormalizingVector 
AcorrSynNA/=NormalizingVector
AcorrNonsynNA/=NormalizingVector  
CrosscorrNA[:nbins]/=NormalizingVector
CrosscorrNA[nbins:2*nbins]/=NormalizingVector


plt.figure()
plt.plot(AcorrSynHA[1:]/np.mean(AcorrSynHA[-10:]), label = 'HAsyn'+' asym: '+ str(round(np.mean(AcorrSynHA[-10:]), 4)))
plt.plot(AcorrNonsynHA[1:]/np.mean(AcorrNonsynHA[-10:]), label = 'HAnonsyn'+' asym: '+ str(round(np.mean(AcorrNonsynHA[-10:]), 4)))
plt.plot(AcorrSynNA[1:]/np.mean(AcorrSynNA[-10:]), label = 'NAsyn'+' asym: '+ str(round(np.mean(AcorrSynNA[-10:]), 4)))
plt.plot(AcorrNonsynNA[1:]/np.mean(AcorrNonsynNA[-10:]), label = 'NAnonsyn'+' asym: '+ str(round(np.mean(AcorrNonsynNA[-10:]), 4)))
plt.axhline(y=1,linestyle='--',color='k')
plt.xlabel('Separation(codons)',fontsize=15)
plt.ylabel('Autocorrelation',fontsize=15)           
plt.legend()
plt.show()
plt.savefig("Plots/AutocorrHA_NA.png")

plt.figure()
plt.plot(CrosscorrHA[1:2*nbins]/np.mean(CrosscorrHA[-10+2*nbins:2*nbins]), label = 'HAcross'+' asym: '+ str(round(np.mean(CrosscorrHA[-10+2*nbins:2*nbins]), 4)))
plt.plot(CrosscorrNA[1:2*nbins]/np.mean(CrosscorrNA[-10+2*nbins:2*nbins]), label = 'NAcross'+' asym: '+ str(round(np.mean(CrosscorrNA[-10+2*nbins:2*nbins]), 4)))
plt.axhline(y=1,linestyle='--',color='k')
plt.xlabel('Separation(codons)',fontsize=15)
plt.ylabel('Crosscorrelation',fontsize=15)
plt.legend()
plt.show()
plt.savefig("Plots/CrosscorrHA_NA.png")    