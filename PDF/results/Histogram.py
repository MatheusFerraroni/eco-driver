import csv
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
import math

x = []
y = []

x1 = []
y1 = []

x2 = []
y2 = []

x3 = []
y3 = []

a1 = 'fuzzy_2'
a2 = 'fuzzy_4'
a3 = 'modelo'
a4 = 'sumo'

arquivo = 'Empirical_Probability_Density'

with open(a1+ '.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=':', quotechar='|')    
    for row in spamreader:
        x.append(int(row[0]))
        y.append(float(row[1]))

x = np.array(x)
y = np.array(y)

with open(a2 + '.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=':', quotechar='|')    
    for row1 in spamreader:
        x1.append(int(row1[0]))
        y1.append(float(row1[1]))

x1 = np.array(x1)
y1 = np.array(y1)

with open(a3 + '.csv', newline='') as csvfile:
    spamreader2 = csv.reader(csvfile, delimiter=':', quotechar='|')    
    for row2 in spamreader2:
        x2.append(int(row2[0]))
        y2.append(float(row2[1]))

x2 = np.array(x2)
y2 = np.array(y2)

with open(a4 + '.csv', newline='') as csvfile:
    spamreader3 = csv.reader(csvfile, delimiter=':', quotechar='|')    
    for row3 in spamreader3:
        x3.append(int(row3[0]))
        y3.append(float(row3[1]))

x3 = np.array(x3)
y3 = np.array(y3)

def plott(x,x1,x2,x3,y,y1,y2,y3):    

    limInf = 85
    limSup = 102
    space = 0.6

    new = []
    for i in range(len(x)):
        if i >= limInf and i <= limSup:
            new.append(int(x[i]))

    fig = plt.figure(figsize=(15,5))
    plt.ylim(0, max(y1)+5) 
    plt.xlim(limInf, limSup)    
        
    plt.bar(x - 0.43*space, y2, label='Neural Network', color='tab:blue', width=0.2)
    plt.bar(x - 0.1*space, y, label='Fuzzy1', color='tab:orange', width=0.2)        
    plt.bar(x + 0.2*space, y1, label='Fuzzy2', color='tab:green', width=0.2)
    plt.bar(x + 0.5*space, y3, label='SUMO', color='tab:red', width=0.2)  
    plt.ylabel('Empirical Probability Density Function (%)', fontweight="bold")
    plt.xlabel('Speed (km/h)', fontweight="bold")

    plt.xticks(new)
    plt.legend(numpoints=1, loc="upper left", ncol=2)  # ,bbox_to_anchor=(-0.02, 1.15)
    plt.grid(True, which="both", ls="-", linewidth=0.1, color='0.10', zorder=0)
    name = arquivo
    fig.savefig(name+'.png', bbox_inches='tight')
    plt.close(fig)          

plott(x,x1,x2,x3,y,y1,y2,y3)