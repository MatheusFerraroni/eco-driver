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

x = np.arange(30)
print(x)
mean_speed_fuzzy = []
mean_speed_model = []
mean_speed_sumo = []

total_fuel_fuzzy = []
total_fuel_model = []
total_fuel_sumo = []

for m in mapas:
    # print(m,dados[m]["Fuzzy"][-1]['total_fuel'])
    # print(m,dados[m]["Fuzzy"][-1]['mean_speed'])
    # print(m,dados[m]["Fuzzy"][-1]['step'])

    mean_speed_fuzzy.append(dados[m]["Fuzzy"][-1]['mean_speed'])
    mean_speed_model.append(dados[m]["Model"][-1]['mean_speed'])
    mean_speed_sumo.append(dados[m]["Krauss"][-1]['mean_speed'])

    total_fuel_fuzzy.append(dados[m]["Fuzzy"][-1]['total_fuel'])
    total_fuel_model.append(dados[m]["Model"][-1]['total_fuel'])
    total_fuel_sumo.append(dados[m]["Krauss"][-1]['total_fuel'])





width = 0.30 

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, total_fuel_fuzzy, width, label='Fuzzy')
rects2 = ax.bar(x, total_fuel_model, width, label='Model')
rects3 = ax.bar(x + width/2, total_fuel_sumo, width, label='Sumo')


plt.show()


