import json
import os
import math

import matplotlib.pyplot as plt
import matplotlib.markers as plm
import numpy as np
import matplotlib.colors as mcolors

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), np.std(a)
    h = 3.291 * (se/math.sqrt(n))
    return (m, h)

color1 = "tab:blue"
color2 = "tab:orange"
color3 = "tab:green"
color4 = "tab:red"


folder = "./mapas_validation/"
mapas = os.listdir(folder)  
mapas = [mapa for mapa in mapas if mapa.split(".")[-1]=="xml" and mapa.split(".")[-2]=="net"]

mapas.sort()  

f = open("final_res_complete.json","r")

dados = json.loads(f.read())
f.close()

x = np.arange(15)

mean_speed_fuzzy = []
mean_speed_fuzzyv = []
mean_speed_model = []
mean_speed_sumo = []

total_fuel_fuzzy = []
total_fuel_fuzzyv = []
total_fuel_model = []
total_fuel_sumo = []

step_fuzzy = []
step_fuzzyv = []
step_model = []
step_sumo = []


i=0

for m in mapas:

    if(i<15):
        mean_speed_fuzzy.append(dados[m]["Fuzzy"][-1]['mean_speed']*3.6)
        mean_speed_fuzzyv.append(dados[m]["Fuzzy2"][-1]['mean_speed']*3.6)
        mean_speed_model.append(dados[m]["Model"][-1]['mean_speed']*3.6)
        mean_speed_sumo.append(dados[m]["KraussPS"][-1]['mean_speed']*3.6)

        total_fuel_fuzzy.append(dados[m]["Fuzzy"][-1]['total_fuel'])
        total_fuel_fuzzyv.append(dados[m]["Fuzzy2"][-1]['total_fuel'])
        total_fuel_model.append(dados[m]["Model"][-1]['total_fuel'])
        total_fuel_sumo.append(dados[m]["KraussPS"][-1]['total_fuel'])

        step_fuzzy.append(dados[m]["Fuzzy"][-1]['step'])
        step_fuzzyv.append(dados[m]["Fuzzy2"][-1]['step'])
        step_model.append(dados[m]["Model"][-1]['step'])
        step_sumo.append(dados[m]["KraussPS"][-1]['step'])
    i+=1


data_list = [[mean_speed_fuzzy, mean_speed_fuzzyv, mean_speed_model, mean_speed_sumo],
            [total_fuel_fuzzy, total_fuel_fuzzyv, total_fuel_model, total_fuel_sumo],
            [step_fuzzy, step_fuzzyv, step_model, step_sumo]]

for i in range(len(data_list)):
    mini = np.amin(data_list[i])
    maxi = np.amax(data_list[i])
    
    for j in range(len(data_list[i])):

        for k in range(len(data_list[i][j])):

            data_list[i][j][k] = data_list[i][j][k]/maxi
            # data_list[i][j][k] = (data_list[i][j][k] - mini) / (maxi - mini)


for i in range(len(data_list)):

    print(f'{np.mean(data_list[i][0])}, {np.mean(data_list[i][1])}, {np.mean(data_list[i][2])}, {np.mean(data_list[i][3])}')
    print(f'{np.std(data_list[i][0])}, {np.std(data_list[i][1])}, {np.std(data_list[i][2])}, {np.std(data_list[i][3])}')
    print('')


fig, ax = plt.subplots()

space = [1*0.2, 2*0.2, 3*0.2, 4*0.2]
labels = ['Mean Speed', 'Total Fuel', 'Time']
xticklabels = ['Fuzzy 1', 'Fuzzy 2', 'Neural Network', 'Sumo']

# print(data_list[i][3])
# data_list[i][3] = [1.0]*15
# print(data_list[i][3])

for i in range(0, 3):

    m1, s1 = mean_confidence_interval(data_list[i][0])
    m2, s2 = mean_confidence_interval(data_list[i][1])
    m3, s3 = mean_confidence_interval(data_list[i][2])
    m4, s4 = mean_confidence_interval(data_list[i][3])
    # print(m1, s1)
    # print(m2, s2)
    # print(m3, s3)
    # print(m4, s4)

    color = "red"
    hatch = '|'

    if i==0:
        color='#1d3557'
        hatch = '++'
    elif i==1:
        color='#457b9d'
        hatch = ''
    elif i==2:
        color='#a8dadc'
        hatch = '..'

    ax.bar(np.arange(0, 4) + space[i],
            [m1, 
             m2, 
             m3, 
             m4],
            yerr=[s1, 
                  s2, 
                  s3,
                  s4],
            label=labels[i],
            width=0.2,
            alpha=0.9,
            edgecolor='black',
            hatch=hatch,
            color=color,
            capsize=2)

ax.set_ylabel('Scaled Result', fontweight='bold')
ax.set_xlabel('Strategies', fontweight='bold')
ax.set_xticks(np.arange(len(xticklabels)) + 0.4)
ax.set_xticklabels(xticklabels)
ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1),
              ncol=4, fancybox=True, shadow=True)

ax.grid(linestyle='--', axis='y', alpha=0.4, color='black')

ax.set_ylim(0.5, 1.01)

fig.savefig('test.png', bbox_inches='tight')