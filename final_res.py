import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import matplotlib.pyplot as plt
import argparse
import json
import sys
from datetime import datetime
import threading
import socket
import subprocess
import time
from keras.models import Sequential
from keras.layers import Dense
import shutil
import fuzzy_in_two
import fuzzy_in_three


caminho_veiculo = [
'AA0AB0','AB0AC0','AC0AD0','AD0AE0','AE0AF0','AF0AG0','AG0AH0','AH0AI0','AI0AJ0','AJ0AK0','AK0AL0','AL0AM0','AM0AN0','AN0AO0',
'AO0AP0','AP0AQ0','AQ0AR0','AR0AS0','AS0AT0','AT0AU0','AU0AV0','AV0AW0','AW0AX0','AX0AY0','AY0AZ0','AZ0BA0','BA0BB0','BB0BC0','BC0BD0','BD0BE0',
'BE0BF0','BF0BG0','BG0BH0','BH0BI0','BI0BJ0','BJ0BK0','BK0BL0','BL0BM0','BM0BN0','BN0BO0'
    ]

max_speed_caminhao = 30 # ~ 108km/h
max_dif_altura = 50
extras_mapas = None
z_add = 100

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Environment variable SUMO_HOME not defined")
import traci

def get_model():
    model = Sequential()
    model.add(Dense(30, input_shape=(10,)))
    model.add(Dense(20))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer='adam', loss='categorical_crossentropy')

    return model

def calculate_new_fuel(instant_fuel, instant_slope, max_slope, instant_acell, max_accel):

    total_accel = instant_acell/max_accel
    total_slope = instant_slope/max_slope

    if total_slope>0:
        instant_fuel = instant_fuel*(1+total_accel)

    return instant_fuel

def getClosest(arr, n, target):

    if type(arr) is not list:
        return arr
    if (target <= arr[0]["x"]): 
        return arr[0]
    if (target >= arr[n - 1]["x"]): 
        return arr[n - 1]


    # Doing binary search 
    i = 0; j = n; mid = 0
    while (i < j):  
        mid = (i + j) // 2
  
        if (arr[mid]["x"] == target): 
            return arr[mid] 
  
        # If target is less than array  
        # element, then search in left 
        if (target < arr[mid]["x"]) : 
  
            # If target is greater than previous 
            # to mid, return closest of two 
            if (mid > 0 and target > arr[mid - 1]["x"]): 
                return getClosest(arr[mid - 1], arr[mid], target) 
  
            # Repeat for left half  
            j = mid 
          
        # If target is greater than mid 
        else : 
            if (mid < n - 1 and target < arr[mid + 1]["x"]): 
                return getClosest(arr[mid], arr[mid + 1], target) 
                  
            # update i 
            i = mid + 1
          
    # Only single element left after search 
    return arr[mid] 


def get_info_pos(mapa, x):
    global extras_mapas
    if extras_mapas==None:
        extras_mapas = {}
        folder = "./mapas_validation/"
        mapas = os.listdir(folder)
        mapas_todos = [mapa for mapa in mapas if mapa.split(".")[-1]=="xml" and mapa.split(".")[-2]=="net"]
        for m in mapas_todos:
            f = open(folder+m.replace(".net.xml",".extras"),"r")
            extras_mapas[m] = json.loads(f.read())
            f.close()

    d = extras_mapas[mapa]
    return getClosest(d,len(d),x)



def converter(gen):
    if type(gen)==list:
        ret = []
        for w in gen:
            ret.append(converter(w))
        return np.array(ret, dtype=object)

    return gen

class UnusedPortLock:
    lock = threading.Lock()

    def __init__(self):
        self.acquired = False

    def __enter__(self):
        self.acquire()

    def __exit__(self):
        self.release()

    def acquire(self):
        if not self.acquired:
            UnusedPortLock.lock.acquire()
            self.acquired = True

    def release(self):
        if self.acquired:
            UnusedPortLock.lock.release()
            self.acquired = False


def run(model, mapa):


    f_2 = fuzzy_in_two.Algorithm()
    f_3 = fuzzy_in_three.Algorithm()

    step = 0

    traci.route.add("trip", caminho_veiculo)
    traci.vehicle.add("caminhao", "trip")
    if type(model)==str and model!="fuzzy":
        traci.vehicle.setParameter("caminhao","carFollowModel",model)
        # print("entrou",model)
    else:
        traci.vehicle.setParameter("caminhao","carFollowModel","KraussPS")
        # print("padrao")
    traci.vehicle.setVehicleClass("caminhao","truck")
    traci.vehicle.setShapeClass("caminhao","truck")
    traci.vehicle.setEmissionClass("caminhao","PHEMlight/PC_G_EU4")
    traci.vehicle.setMaxSpeed("caminhao",max_speed_caminhao) 
    r = 1
    max_angulo = 60

    total_fuel = 0

    dados_retorno = []
    try:
        while step == 0 or traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()
            step += 1

            try:
                speed = traci.vehicle.getSpeed("caminhao")
                angle = traci.vehicle.getSlope("caminhao")
                x, y, z = traci.vehicle.getPosition3D("caminhao")

                max_acel = traci.vehicle.getAccel("caminhao")
                inst_acel = traci.vehicle.getAcceleration("caminhao")



                inf10 = get_info_pos(mapa, x+10)
                inf20 = get_info_pos(mapa, x+20)
                inf30 = get_info_pos(mapa, x+30)
                inf40 = get_info_pos(mapa, x+40)
                inf50 = get_info_pos(mapa, x+50)
                inf60 = get_info_pos(mapa, x+60)
                inf70 = get_info_pos(mapa, x+70)
                inf100 = get_info_pos(mapa, x+100)



                if type(model)!=str and model!="fuzzy":
                    angle /= 90
                    # inf10 = inf10["angle"]/90
                    # inf30 = inf30["angle"]/90
                    # inf50 = inf50["angle"]/90
                    # inf70 = inf70["angle"]/90
                    # entrada = [speed/max_speed_caminhao, angle, inf10, inf30, inf50, inf70]


                    angle /= max_angulo
                    inf10 = inf10["angle"]/max_angulo
                    inf20 = inf20["angle"]/max_angulo
                    inf30 = inf30["angle"]/max_angulo
                    inf40 = inf40["angle"]/max_angulo
                    inf50 = inf50["angle"]/max_angulo
                    inf60 = inf60["angle"]/max_angulo
                    inf70 = inf70["angle"]/max_angulo
                    inf100 = inf100["angle"]/max_angulo


                    entrada = [speed/max_speed_caminhao, angle, inf10, inf20, inf30, inf40, inf50, inf60, inf70, inf100]


                    r = model.predict(np.array([np.array(entrada)]))[0][0]


                    if r<0.1:
                        r = 0.1
                    traci.vehicle.setSpeed("caminhao",r*max_speed_caminhao)
                elif model=="fuzzy":
                    normalization = 1 #90
                    angle /= normalization
                    inf10 = inf10["angle"]/normalization
                    inf30 = inf30["angle"]/normalization
                    inf50 = inf50["angle"]/normalization
                    inf70 = inf70["angle"]/normalization

                    # FUZZY
                    r = f_2.findSpeed(speed,angle, inf10, inf30, inf50, inf70)

                    traci.vehicle.setSpeed("caminhao",r)

                fuel_last_step = traci.vehicle.getFuelConsumption("caminhao")
                instant_fuel_consuption2 = calculate_new_fuel(fuel_last_step, angle, max_angulo, inst_acel, max_acel)

                total_fuel += fuel_last_step

                dados_retorno.append({
                    "x": x,
                    "y": y,
                    "z": z,
                    "total_fuel": total_fuel,
                    "fuel_last_step": fuel_last_step,
                    "speed_recommended": r*max_speed_caminhao,
                    "step": step,
                    "speed": speed
                    })
            except Exception as e:
                print("######################")
                print(e)
                print("######################")
                continue
                # pass





    except Exception as e:
        print("######################")
        print(e)
        print("######################")
        raise

    return dados_retorno


def find_unused_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.bind(('127.0.0.1', 0))
    sock.listen(socket.SOMAXCONN)
    ipaddr, port = sock.getsockname()
    sock.close()

    return port

def terminate_sumo(sumo):
    if sumo.returncode != None:
        os.system("taskkill.exe /F /im sumo.exe")
        time.sleep(1)

def start_simulation(sumo, scenario, network, model, mapa):
    unused_port_lock = UnusedPortLock()
    unused_port_lock.__enter__()
    remote_port = find_unused_port()

    sumo = subprocess.Popen([sumo, "-c", scenario, "--device.emissions.probability", "1.0", "--remote-port", str(remote_port), "--duration-log.statistics","--log", "logfile.txt"], stdout=sys.stdout, stderr=sys.stderr)    
    unused_port_lock.release()


    try:
        traci.init(remote_port)            
        return run(model, mapa)
    except Exception as e:
        print(e)
        raise
    finally:
        print("Terminating SUMO")
        terminate_sumo(sumo)
        unused_port_lock.__exit__()


def plow(dados, extras, nome):
    xs = []
    ys = []
    ys_green_above = []
    ys_green_below = []


    fig, ax = plt.subplots(4,1,figsize=(20,5))
    for i in range(len(extras)):
        # if i>10: break

        inf = extras[i]
        xs.append(inf["x"])
        ys.append(inf["z"]+z_add)
        ys_green_above.append(inf["z"]+z_add+10)
        ys_green_below.append(inf["z"]+z_add-10)


        # if i%50==0 and i%100!=0:
        #     ax[0].annotate(str(round(inf["angle"],1)),
        #                 xy=(inf["x"], inf["z"]+z_add+5), xycoords='data',
        #                 xytext=(5, 40), textcoords='offset points',
        #                 arrowprops=dict(arrowstyle="->"),
        #                 horizontalalignment='right', verticalalignment='bottom')

    # ax[0].set_ylim(0,300)
    ax[0].patch.set_facecolor('#87d3e0')
    ax[0].set_xlim(-20,xs[-1]+20)
    ax[1].set_xlim(-20,xs[-1]+20)
    ax[2].set_xlim(-20,xs[-1]+20)
    ax[3].set_xlim(-20,xs[-1]+20)
    ax[0].stackplot(xs, ys_green_above, color="#269126")
    ax[0].stackplot(xs, ys, color="#000000")
    ax[0].stackplot(xs, ys_green_below, color="#269126")
    ax[0].set_title('Elevation for Map '+nome.replace(".net.xml",""))
    ax[0].set_xlabel('Distance (m)')
    ax[0].set_ylabel('Height (h)')


    entradas = [
        "Model",
        "Fuzzy",
        "Krauss",
        "KraussOrig1",
        "KraussPS",
        "PWagner2009",
        "IDM",
        "Wiedemann",
        "W99",
    ]

    for e in entradas:
        xs = []
        ys = []
        for a in dados[e]:
            xs.append(a['x'])
            ys.append(a['fuel_last_step'])
        if len(xs)>0:
            ax[1].plot(xs, ys, label=e)



    ax[1].set_xlabel('Distance (m)')
    ax[1].set_ylabel('Instant Fuel')

    # ax[1].legend()


    for e in entradas:
        xs = []
        ys = []
        for a in dados[e]:
            xs.append(a['x'])
            ys.append(a['speed'])
        if len(xs)>0:
            ax[2].plot(xs, ys, label=e)



    if len(dados["Model"])>0:
        xs = []
        ys = []
        for a in dados["Model"]:
            xs.append(a['x'])
            ys.append(a['speed_recommended'])
        if len(xs)>0:
            ax[2].plot(xs, ys, dashes=[6, 2], label="Model Recommended", color="#bd1111")
            ax[3].plot([], [], dashes=[6, 2], label="Model Recommended", color="#bd1111")


    ax[2].set_xlabel('Distance (m)')
    ax[2].set_ylabel('Speed')
    # ax[2].legend()

    for e in entradas:
        xs = []
        ys = []
        total = 0
        for a in dados[e]:
            xs.append(a['x'])
            ys.append(a['total_fuel'])
            total = a['total_fuel']

        total = round(total,1)
        if len(xs)>0:
            ax[3].plot(xs, ys, label="{} ({})".format(e,total))



    ax[3].set_xlabel('Distance (m)')
    ax[3].set_ylabel('Total Fuel')
    ax[3].legend()
    ax[3].legend(loc='lower center', bbox_to_anchor=(0.5, -2),
              ncol=3, fancybox=True, shadow=True)

    plt.savefig("./mapas_validation/FINAL_"+nome+".png", bbox_inches="tight")
    plt.close()
    # break



def main(arquivo):
    f = open(arquivo,"r")
    dado = json.loads(f.read())
    f.close()
    gen = dado["historic"][-1]["best_genome"]
    gen = converter(gen)
    model = get_model()
    model.set_weights(gen)



    folder = "./mapas_validation/"
    mapas = os.listdir(folder)

    mapas = [mapa for mapa in mapas if mapa.split(".")[-1]=="xml" and mapa.split(".")[-2]=="net"]
    
    resultados_obtidos = {}
    for m in mapas:
        resultados_obtidos[m] = {"Model":[],"Krauss":[],"KraussOrig1":[],"KraussPS":[],"PWagner2009":[],"IDM":[],"Wiedemann":[],"W99":[],"Fuzzy":[]}
        print("_______Model______________")
        resultados_obtidos[m]["Model"] = start_simulation("sumo", (folder+m).replace(".net.xml",".sumo.cfg"), (folder+m), model, m)
        print("_______Krauss______________")
        resultados_obtidos[m]["Krauss"]   = start_simulation("sumo", (folder+m).replace(".net.xml",".sumo.cfg"), (folder+m), "Krauss", m)
        print("_______KraussOrig1______________")
        resultados_obtidos[m]["KraussOrig1"]   = start_simulation("sumo", (folder+m).replace(".net.xml",".sumo.cfg"), (folder+m), "KraussOrig1", m)
        print("_______KraussPS______________")
        resultados_obtidos[m]["KraussPS"]   = start_simulation("sumo", (folder+m).replace(".net.xml",".sumo.cfg"), (folder+m), "KraussPS", m)
        print("_______PWagner2009______________")
        resultados_obtidos[m]["PWagner2009"]   = start_simulation("sumo", (folder+m).replace(".net.xml",".sumo.cfg"), (folder+m), "PWagner2009", m)
        print("_______IDM______________")
        resultados_obtidos[m]["IDM"]   = start_simulation("sumo", (folder+m).replace(".net.xml",".sumo.cfg"), (folder+m), "IDM", m)
        print("_______Wiedemann______________")
        resultados_obtidos[m]["Wiedemann"]   = start_simulation("sumo", (folder+m).replace(".net.xml",".sumo.cfg"), (folder+m), "Wiedemann", m)
        print("_______W99______________")
        resultados_obtidos[m]["W99"]   = start_simulation("sumo", (folder+m).replace(".net.xml",".sumo.cfg"), (folder+m), "W99", m)
        print("_______Fuzzy______________")
        resultados_obtidos[m]["Fuzzy"] = start_simulation("sumo", (folder+m).replace(".net.xml",".sumo.cfg"), (folder+m), "fuzzy", m)


        file = open(folder+m.replace(".net.xml",".extras"),"r")
        extras = json.loads(file.read())
        file.close()


        plow(resultados_obtidos[m], extras, m)
        # break


if __name__ == '__main__':
    a = "./results/10_10_True_0.1.json"
    main(a)
