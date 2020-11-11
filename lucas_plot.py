import matplotlib.pyplot as plt
import matplotlib.markers as plm
import numpy as np
import json
import os
import matplotlib.colors as mcolors

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

            data_list[i][j][k] = (data_list[i][j][k] - mini) / (maxi - mini)


for i in range(len(data_list)):

    print(f'{np.mean(data_list[i][0])}, {np.mean(data_list[i][1])}, {np.mean(data_list[i][2])}, {np.mean(data_list[i][3])}')
    print(f'{np.std(data_list[i][0])}, {np.std(data_list[i][1])}, {np.std(data_list[i][2])}, {np.std(data_list[i][3])}')
    print('')


fig, ax = plt.subplots()

space = [1*0.2, 2*0.2, 3*0.2, 4*0.2]
labels = ['Mean Speed', 'Total Fuel', 'Steps']
xticklabels = ['Fuzzy 1', 'Fuzzy 2', 'Model', 'Sumo']

for i in range(0, 3):

    ax.bar(np.arange(0, 4) + space[i],
            [np.mean(data_list[i][0]), 
             np.mean(data_list[i][1]), 
             np.mean(data_list[i][2]), 
             np.mean(data_list[i][3])],
            yerr=[np.std(data_list[i][0]), 
                    np.std(data_list[i][1]), 
                    np.std(data_list[i][2]),
                    np.std(data_list[i][3])],
            label=labels[i],
            width=0.2,
            alpha=0.9,
            edgecolor='black',
            capsize=2)

ax.set_ylabel('Normalized Result', fontweight='bold')
ax.set_xlabel('Strategies', fontweight='bold')
ax.set_xticks(np.arange(len(xticklabels)) + 0.4)
ax.set_xticklabels(xticklabels)
ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1),
              ncol=4, fancybox=True, shadow=True)

ax.grid(linestyle='--', axis='y', alpha=0.4, color='black')

fig.savefig('test.png', bbox_inches='tight')