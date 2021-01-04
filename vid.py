import json
import numpy as np
import matplotlib.pyplot as plt
import os, shutil
import matplotlib.gridspec as gridspec
from PIL import Image
import glob
import sys
import matplotlib.colors as mcolors
import csv

color1 = "tab:blue"
color2 = "tab:orange"
color3 = "tab:green"
color4 = "tab:red"

labels = [' ', 'Neural Network', ' ', 'Fuzzy1', ' ', 'Fuzzy2',  ' ', 'SUMO', ' ']

z_add = 30

def main():

    if not os.path.isdir("./video"):
        os.mkdir("./video")
    
    imgs = glob.glob("./video/*.png")
    for i in imgs:
        os.remove(i)
    imgs = glob.glob("./video/*.gif")
    for i in imgs:
        os.remove(i)


    f = open("final_res_complete.json","r")
    dados = json.loads(f.read())
    f.close()


    folder = "./mapas_validation/"
    mapas = os.listdir(folder)  
    mapas = [mapa for mapa in mapas if mapa.split(".")[-1]=="xml" and mapa.split(".")[-2]=="net"]

    mapas.sort()


    tecs = ["Model", "Fuzzy", "Fuzzy2", "KraussPS"]


    for m in mapas:


        f = open(folder+m.replace(".net.xml",".extras"),"r")
        mapa = json.loads(f.read())
        f.close()

        xs_mapa = []
        ys_mapa = []
        ys_mapa_green_above = []
        ys_mapa_green_below = []

        for i in range(len(mapa)):
            inf = mapa[i]
            xs_mapa.append(inf["x"])
            ys_mapa.append(inf["z"]+z_add)
            ys_mapa_green_above.append(inf["z"]+z_add+5)
            ys_mapa_green_below.append(inf["z"]+z_add-5)



        max_step = 0
        for t in tecs:
            max_step = max(max_step, len(dados[m][t]))

        frames = []
        for step in range(0,max_step,1):


            # fig, ax = plt.subplots(2,1,figsize=(20,5))

            fig = plt.figure(figsize=(16,9),tight_layout=True)
            gs = gridspec.GridSpec(3, 3)
            ax = fig.add_subplot(gs[0, :])
            ax.patch.set_facecolor('#87d3e0')
            ax.set_xlim(-20,xs_mapa[-1]+20)
            ax.set_ylim(0,60)
            ax.stackplot(xs_mapa, ys_mapa_green_above, colors=['#269126'])
            ax.stackplot(xs_mapa, ys_mapa, colors=["#000000"])
            ax.stackplot(xs_mapa, ys_mapa_green_below, colors=["#269126"])
            ax.set_title('Map '+m.replace(".net.xml",""))
            ax.set_xlabel('Distance [m]')
            ax.set_ylabel('Height [m]')

            model_x = -100
            model_z = -100
            model_speed = -100
            model_instant_fuel = -100
            model_total_fuel = -100

            fuzzy_x = -100
            fuzzy_z = -100
            fuzzy_speed = -100
            fuzzy_instant_fuel = -100
            fuzzy_total_fuel = -100

            fuzzy2_x = -100
            fuzzy2_z = -100
            fuzzy2_speed = -100
            fuzzy2_instant_fuel = -100
            fuzzy2_total_fuel = -100

            sumo_x = -100
            sumo_z = -100
            sumo_speed = -100
            sumo_instant_fuel = -100
            sumo_total_fuel = -100

            for t in tecs:

                if len(dados[m][t]) > step:
                    x,y,z = dados[m][t][step]["x"],  dados[m][t][step]["y"],  dados[m][t][step]["z"]
                    speed = dados[m][t][step]["speed"]
                    total_fuel = dados[m][t][step]["total_fuel"]
                    fuel_last_step = dados[m][t][step]["fuel_last_step"]
                    
                    if x>xs_mapa[-1]: continue
                    if t=="Model":
                        model_x = x
                        model_z = z+z_add
                        model_speed = speed*3.6
                        model_instant_fuel = fuel_last_step
                        model_total_fuel = total_fuel
                    elif t=="Fuzzy":
                        fuzzy_x = x
                        fuzzy_z = z+z_add
                        fuzzy_speed = speed*3.6
                        fuzzy_instant_fuel = fuel_last_step
                        fuzzy_total_fuel = total_fuel
                    elif t=="Fuzzy2":
                        fuzzy2_x = x
                        fuzzy2_z = z+z_add
                        fuzzy2_speed = speed*3.6
                        fuzzy2_instant_fuel = fuel_last_step
                        fuzzy2_total_fuel = total_fuel
                    elif t=="KraussPS":
                        sumo_x = x
                        sumo_z = z+z_add
                        sumo_speed = speed*3.6
                        sumo_instant_fuel = fuel_last_step
                        sumo_total_fuel = total_fuel
 

            # ax.scatter([model_x,fuzzy_x,fuzzy2_x, sumo_x],[model_z,fuzzy_z,fuzzy2_z, sumo_z], s=80, c=["#FF0000","#00FF00","#0000FF","#FFF0F0"])
            ax.scatter(model_x, model_z, s=80, color=color1, label='Neural Network')
            ax.scatter(fuzzy_x, fuzzy_z, s=80, color=color2, label='Fuzzy1')
            ax.scatter(fuzzy2_x, fuzzy2_z, s=80, color=color3, label='Fuzzy2')
            ax.scatter(sumo_x, sumo_z, s=80, color=color4, label='SUMO')

            ax.legend(loc='lower center', bbox_to_anchor=(0.8, 1.0),  ncol=4, fancybox=True, shadow=True)


            ax.text(40, 62, "Time: "+str(step)+" s", ha='left')

            def autolabel(rects):
                for rect in rects:

                    height = int(rect.get_height())
                    
                    ax.annotate('{}'.format(height),
                                xy=(rect.get_x() + rect.get_width() / 2, height),
                                xytext=(1, 3),  # 3 points vertical offset
                                textcoords="offset points",
                                ha='center', va='bottom', rotation=0,
                                horizontalalignment='center', verticalalignment='center')

            ax = fig.add_subplot(gs[1, 0])
            # ax.set_xlabel("Approach")
            ax.set_ylabel("Speed [km/h]")
            ax.set_ylim(0,120)
            ax.set_xticklabels(labels)
            ax.set_xlim(0,4)
            ax.grid()
            rects1 = ax.bar([0.5,1.5,2.5,3.5], [model_speed, fuzzy_speed, fuzzy2_speed, sumo_speed], color=[color1,color2,color3,color4])
            autolabel(rects1)
          

            ax = fig.add_subplot(gs[1, 1])
            # ax.set_xlabel("Approach")
            ax.set_ylabel("Instant Fuel [ml/s]")
            ax.set_ylim(0,40)
            ax.set_xticklabels(labels)
            ax.set_xlim(0,4)
            ax.grid()
            rects2 = ax.bar([0.5,1.5,2.5,3.5], [model_instant_fuel, fuzzy_instant_fuel, fuzzy2_instant_fuel, sumo_instant_fuel], color=[color1,color2,color3,color4])
            autolabel(rects2)

            ax = fig.add_subplot(gs[1, 2])
            # ax.set_xlabel("Approach")
            ax.set_ylabel("Total Fuel [ml]")
            ax.set_ylim(0,3000)
            ax.set_xticklabels(labels)
            ax.set_xlim(0,4)
            ax.grid()
            rects3 = ax.bar([0.5,1.5,2.5,3.5], [model_total_fuel, fuzzy_total_fuel, fuzzy2_total_fuel, sumo_total_fuel], color=[color1,color2,color3,color4])
            # ax.bar([0.5,1.5,2.5,3.5], model_total_fuel, color=color1, label='Neural Network')
            # ax.bar([0.5,1.5,2.5,3.5], fuzzy_total_fuel, color=color2, label='Fuzzy1')
            # ax.bar([0.5,1.5,2.5,3.5], fuzzy2_total_fuel, color=color3, label='Fuzzy2')
            # ax.bar([0.5,1.5,2.5,3.5], sumo_total_fuel, color=color4, label='SUMO')
     


           
            autolabel(rects3)
            # autolabel(rects4)

            


            plt.savefig("./video/"+str(step)+".png", bbox_inches="tight")
            plt.close()


            new_frame = Image.open("./video/"+str(step)+".png")
            frames.append(new_frame)




        frames[0].save('./video/'+m+'.gif', format='GIF', 
                       append_images=frames[1:],
                       save_all=True,
                       duration=300, loop=0)


        imgs = glob.glob("./video/*.png")
        for i in imgs:
            os.remove(i)

        # break


if __name__ == '__main__':
    main()