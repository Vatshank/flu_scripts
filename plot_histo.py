import os
import matplotlib.pyplot as plt

yearlist = os.listdir('Out1/')
histo = {}
for year in yearlist:
    segments = os.listdir("Out1/"+year+"/")
    count = 0
    for segment in segments:
        count += len(os.listdir("Out1/"+year+"/"+segment+"/"))
    if(int(year)<13):
        yearname = "20"+year
    else:
        yearname = "19"+year
    histo[int(yearname)] = count

N = histo
plt.close()
plt.bar(N.keys(), N.values(), align='center', width = 0.5)
plt.xlabel('Collection Year')
plt.ylabel('Total Number of Segments (HA + NA)')
plt.show()
