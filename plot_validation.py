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

x = np.arange(10)

mean_speed_fuzzy = []
mean_speed_fuzzyv = []
mean_speed_model = []
mean_speed_sumo = []

total_fuel_fuzzy = []
total_fuel_fuzzyv = []
total_fuel_model = []
total_fuel_sumo = []

total_fuel_fuzzy2 = []
total_fuel_fuzzyv2 = []
total_fuel_model2 = []
total_fuel_sumo2 = []

step_fuzzy = []
step_fuzzyv = []
step_model = []
step_sumo = []


i=0

for m in mapas:

    #print('m:', m)
    # print(m,dados[m]["Fuzzy"][-1]['total_fuel'])
    # print(m,dados[m]["Fuzzy"][-1]['mean_speed'])
    # print(m,dados[m]["Fuzzy"][-1]['step'])step
    if(i<10):
        mean_speed_fuzzy.append(dados[m]["Fuzzy"][-1]['mean_speed']*3.6)
        mean_speed_fuzzyv.append(dados[m]["Fuzzy2"][-1]['mean_speed']*3.6)
        mean_speed_model.append(dados[m]["Model"][-1]['mean_speed']*3.6)
        mean_speed_sumo.append(dados[m]["KraussPS"][-1]['mean_speed']*3.6)

        total_fuel_fuzzy.append(dados[m]["Fuzzy"][-1]['total_fuel'])
        total_fuel_fuzzyv.append(dados[m]["Fuzzy2"][-1]['total_fuel'])
        total_fuel_model.append(dados[m]["Model"][-1]['total_fuel'])
        total_fuel_sumo.append(dados[m]["KraussPS"][-1]['total_fuel'])

        total_fuel_fuzzy2.append(dados[m]["Fuzzy"][-1]['total_fuel']/5)
        total_fuel_fuzzyv2.append(dados[m]["Fuzzy2"][-1]['total_fuel']/5)
        total_fuel_model2.append(dados[m]["Model"][-1]['total_fuel']/5)
        total_fuel_sumo2.append(dados[m]["KraussPS"][-1]['total_fuel']/5)


        step_fuzzy.append(dados[m]["Fuzzy"][-1]['step'])
        step_fuzzyv.append(dados[m]["Fuzzy2"][-1]['step'])
        step_model.append(dados[m]["Model"][-1]['step'])
        step_sumo.append(dados[m]["KraussPS"][-1]['step'])
    i+=1




print(len(x))
print(len(total_fuel_fuzzy))


width = 0.18
space = 0.18


labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
#labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
fig, ax = plt.subplots()

ax.set_ylim(2000,3000)

ax.bar(x - 1.5*space, total_fuel_model, width, label='Neural Network',  color=color1)
ax.bar(x - 0.5*space, total_fuel_fuzzy, width, label='Fuzzy1',  color=color2)
ax.bar(x + 0.5*space, total_fuel_fuzzyv, width, label='Fuzzy2', color=color3)
ax.bar(x + 1.5*space, total_fuel_sumo, width, label='SUMO', color=color4)

ax.grid(True, which="both", ls="-", linewidth=0.1, color='0.10', zorder=0) 
ax.set_xticklabels(labels)
ax.set_ylabel('Fuel comsuption [ml]')
ax.set_xlabel('Validation Maps')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1),
              ncol=4, fancybox=True, shadow=True)



fig.savefig('plots/fuel.png', bbox_inches='tight')
plt.close(fig)
# plt.show()



fig, ax = plt.subplots()
ax.set_ylim(85,105)

ax.bar(x - 1.5*space, mean_speed_model, width, label='Neural Network',  color=color1)
ax.bar(x - 0.5*space, mean_speed_fuzzy, width, label='Fuzzy1',  color=color2)
ax.bar(x + 0.5*space, mean_speed_fuzzyv, width, label='Fuzzy2', color=color3)
ax.bar(x + 1.5*space, mean_speed_sumo, width, label='SUMO', color=color4)



ax.grid(True, which="both", ls="-", linewidth=0.1, color='0.10', zorder=0) 
ax.set_xticklabels(labels)
ax.set_ylabel('Mean speed [km/s]')
ax.set_xlabel('Validation Maps')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1),
              ncol=4, fancybox=True, shadow=True)


fig.savefig('plots/speed.png', bbox_inches='tight')
plt.close(fig)

fig, ax = plt.subplots()
ax.set_ylim(170,200)

ax.bar(x - 1.5*space, step_model, width, label='Neural Network',  color=color1)
ax.bar(x - 0.5*space, step_fuzzy, width, label='Fuzzy1',  color=color2)
ax.bar(x + 0.5*space, step_fuzzyv, width, label='Fuzzy2', color=color3)
ax.bar(x + 1.5*space, step_sumo, width, label='SUMO', color=color4)



ax.grid(True, which="both", ls="-", linewidth=0.1, color='0.10', zorder=0) 
ax.set_xticklabels(labels)
ax.set_ylabel('Time [sec]')
ax.set_xlabel('Validation Maps')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1),
              ncol=4, fancybox=True, shadow=True)


fig.savefig('plots/time.png', bbox_inches='tight')
plt.close(fig)


fig, ax = plt.subplots()
ax.set_ylim(400,600)


ax.bar(x - 1.5*space, total_fuel_model2, width, label='Neural Network',  color=color1)
ax.bar(x - 0.5*space, total_fuel_fuzzy2, width, label='Fuzzy1',  color=color2)
ax.bar(x + 0.5*space, total_fuel_fuzzyv2, width, label='Fuzzy2', color=color3)
ax.bar(x + 1.5*space, total_fuel_sumo2, width, label='SUMO', color=color4)


ax.grid(True, which="both", ls="-", linewidth=0.1, color='0.10', zorder=0) 
ax.set_xticklabels(labels)
ax.set_ylabel('Fuel comsuption [ml/km]')
ax.set_xlabel('Validation Maps')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1),
              ncol=4, fancybox=True, shadow=True)


fig.savefig('plots/fuel_km.png', bbox_inches='tight')
plt.close(fig)