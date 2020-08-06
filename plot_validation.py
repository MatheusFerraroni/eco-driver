import matplotlib.pyplot as plt
import matplotlib.markers as plm
import numpy as np
import json
import os

folder = "./mapas_validation/"
mapas = os.listdir(folder)  
mapas = [mapa for mapa in mapas if mapa.split(".")[-1]=="xml" and mapa.split(".")[-2]=="net"]

mapas.sort()  

f = open("final_res_complete.json","r")

dados = json.loads(f.read())
f.close()

x = np.arange(10)

mean_speed_fuzzy = []
mean_speed_model = []
mean_speed_sumo = []

total_fuel_fuzzy = []
total_fuel_model = []
total_fuel_sumo = []

i=0

for m in mapas:

    #print('m:', m)
    # print(m,dados[m]["Fuzzy"][-1]['total_fuel'])
    # print(m,dados[m]["Fuzzy"][-1]['mean_speed'])
    # print(m,dados[m]["Fuzzy"][-1]['step'])
    if(i<10):
        mean_speed_fuzzy.append(dados[m]["Fuzzy"][-1]['mean_speed'])
        mean_speed_model.append(dados[m]["Model"][-1]['mean_speed'])
        mean_speed_sumo.append(dados[m]["Krauss"][-1]['mean_speed'])

        total_fuel_fuzzy.append(dados[m]["Fuzzy"][-1]['total_fuel'])
        total_fuel_model.append(dados[m]["Model"][-1]['total_fuel'])
        total_fuel_sumo.append(dados[m]["Krauss"][-1]['total_fuel'])
    i+=1




print(len(x))
print(len(total_fuel_fuzzy))


width = 0.2
space = 0.2


labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
fig, ax = plt.subplots()

ax.set_ylim(2000,3000)


rects1 = ax.bar(x - space, total_fuel_fuzzy, width, label='Fuzzy')
rects2 = ax.bar(x, total_fuel_model, width, label='Neural Network')
rects3 = ax.bar(x + space, total_fuel_sumo, width, label='Sumo')

ax.grid(True, which="both", ls="-", linewidth=0.1, color='0.10', zorder=0) 
ax.set_xticklabels(labels)
ax.set_ylabel('Fuel comsuption [ml]')
ax.set_xlabel('Validation Maps')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1),
              ncol=3, fancybox=True, shadow=True)



fig.savefig('plots/fuel.png', bbox_inches='tight')
plt.close(fig)
# plt.show()



fig, ax = plt.subplots()
ax.set_ylim(25,28.5)

rects1 = ax.bar(x - space, mean_speed_fuzzy, width, label='Fuzzy')
rects2 = ax.bar(x, mean_speed_model, width, label='Neural Network')
rects3 = ax.bar(x + space, mean_speed_sumo, width, label='Sumo')

ax.grid(True, which="both", ls="-", linewidth=0.1, color='0.10', zorder=0) 
ax.set_xticklabels(labels)
ax.set_ylabel('Mean speed [m/s]')
ax.set_xlabel('Validation Maps')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1),
              ncol=3, fancybox=True, shadow=True)


fig.savefig('plots/speed.png', bbox_inches='tight')
plt.close(fig)