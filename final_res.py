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
import fuzzySpeed


caminho_veiculo = ['A0B0', 'B0C0', 'C0D0', 'D0E0', 'E0F0', 'F0G0', 'G0H0', 'H0I0', 'I0J0', 'J0K0', 'K0L0', 'L0M0', 'M0N0', 'N0O0', 'O0P0', 'P0Q0', 'Q0R0', 'R0S0', 'S0T0']
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
    model.add(Dense(18, input_shape=(9,)))
    model.add(Dense(9))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer='adam', loss='categorical_crossentropy')

    return model


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


    g = fuzzySpeed.Algorithm()

    step = 0

    traci.route.add("trip", caminho_veiculo)
    traci.vehicle.add("caminhao", "trip")
    traci.vehicle.setParameter("caminhao","carFollowModel","KraussPS")
    traci.vehicle.setVehicleClass("caminhao","truck")
    traci.vehicle.setShapeClass("caminhao","truck")
    traci.vehicle.setEmissionClass("caminhao","PHEMlight/PC_G_EU4")
    traci.vehicle.setMaxSpeed("caminhao",max_speed_caminhao) 
    r = 1

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


                inf10 = get_info_pos(mapa, x+10)
                inf30 = get_info_pos(mapa, x+30)
                inf50 = get_info_pos(mapa, x+50)
                inf70 = get_info_pos(mapa, x+70)



                if model!=None and model!="fuzzy":
                    angle /= 90
                    # inf10 = inf10["angle"]/90
                    # inf30 = inf30["angle"]/90
                    # inf50 = inf50["angle"]/90
                    # inf70 = inf70["angle"]/90
                    # entrada = [speed/max_speed_caminhao, angle, inf10, inf30, inf50, inf70]

                    inf10 = get_info_pos(mapa, x+10)
                    inf20 = get_info_pos(mapa, x+20)
                    inf30 = get_info_pos(mapa, x+30)
                    inf40 = get_info_pos(mapa, x+40)
                    inf50 = get_info_pos(mapa, x+50)
                    inf60 = get_info_pos(mapa, x+60)
                    inf70 = get_info_pos(mapa, x+70)

                    angle /= 90
                    inf10 = inf10["angle"]/90
                    inf20 = inf20["angle"]/90
                    inf30 = inf30["angle"]/90
                    inf40 = inf40["angle"]/90
                    inf50 = inf50["angle"]/90
                    inf60 = inf60["angle"]/90
                    inf70 = inf70["angle"]/90

                    entrada = [speed/max_speed_caminhao, angle, inf10, inf20, inf30, inf40, inf50, inf60, inf70]
                    r = model.predict(np.array([np.array(entrada)]))[0][0]

                    if r==0:
                        r = 0.01
                    traci.vehicle.setSpeed("caminhao",r*max_speed_caminhao)
                elif model=="fuzzy":
                    normalization = 1 #90
                    angle /= normalization
                    inf10 = inf10["angle"]/normalization
                    inf30 = inf30["angle"]/normalization
                    inf50 = inf50["angle"]/normalization
                    inf70 = inf70["angle"]/normalization

                    r = g.findSpeed(speed/max_speed_caminhao, angle, inf10, inf30, inf50, inf70)

                    traci.vehicle.setSpeed("caminhao",r)
                fuel_last_step = traci.vehicle.getFuelConsumption("caminhao")
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


    fig, ax = plt.subplots(3,1,figsize=(20,4))
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
    ax[0].stackplot(xs, ys_green_above, color="#269126")
    ax[0].stackplot(xs, ys, color="#000000")
    ax[0].stackplot(xs, ys_green_below, color="#269126")
    ax[0].set_title('Elevation for Map '+nome.replace(".net.xml",""))
    ax[0].set_xlabel('Distance (m)')
    ax[0].set_ylabel('Height (h)')


    xs = []
    ys = []
    for a in dados["raw"]:
        xs.append(a['x'])
        ys.append(a['fuel_last_step'])
    ax[1].plot(xs, ys, label="Sumo")


    xs = []
    ys = []
    for a in dados["model"]:
        xs.append(a['x'])
        ys.append(a['fuel_last_step'])
    ax[1].plot(xs, ys, label="Model")

    xs = []
    ys = []
    for a in dados["fuzzy"]:
        xs.append(a['x'])
        ys.append(a['fuel_last_step'])
    ax[1].plot(xs, ys, label="Fuzzy")


    ax[1].set_xlabel('Distance (m)')
    ax[1].set_ylabel('Fuel Consuption')

    ax[1].legend()



    total_raw = 0
    total_model = 0

    xs = []
    ys = []
    for a in dados["raw"]:
        xs.append(a['x'])
        ys.append(a['speed'])
        total_raw = a['total_fuel']

    total_raw = round(total_raw,0)
    ax[2].plot(xs, ys, label="Sumo ({})".format(total_raw))


    xs = []
    ys = []
    for a in dados["model"]:
        xs.append(a['x'])
        ys.append(a['speed'])
        total_model = a['total_fuel']
    total_model = round(total_model,0)
    ax[2].plot(xs, ys, label="Model ({})".format(total_model))

    xs = []
    ys = []
    for a in dados["fuzzy"]:
        xs.append(a['x'])
        ys.append(a['speed'])
        total_model = a['total_fuel']
    total_model = round(total_model,0)
    ax[2].plot(xs, ys, label="Fuzzy ({})".format(total_model))

    xs = []
    ys = []
    for a in dados["model"]:
        xs.append(a['x'])
        ys.append(a['speed_recommended'])
    ax[2].plot(xs, ys, label="Recommended")


    ax[2].set_xlabel('Distance (m)')
    ax[2].set_ylabel('Speed')

    ax[2].legend()



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


    # for _ in range(10):
    #     entrada = [np.random.random(), np.random.uniform(low=-1, high=1), np.random.uniform(low=-1, high=1), np.random.uniform(low=-1, high=1), np.random.uniform(low=-1, high=1), np.random.uniform(low=-1, high=1)]

    #     r = model.predict(np.array([np.array(entrada)]))[0][0]

    #     print(entrada,r)


    folder = "./mapas_validation/"
    mapas = os.listdir(folder)

    mapas = [mapa for mapa in mapas if mapa.split(".")[-1]=="xml" and mapa.split(".")[-2]=="net"]
    
    resultados_obtidos = {}
    for m in mapas:
        resultados_obtidos[m] = {"raw":None, "model":None}
        resultados_obtidos[m]["raw"]   = start_simulation("sumo", (folder+m).replace(".net.xml",".sumo.cfg"), (folder+m), None, m)
        resultados_obtidos[m]["model"] = start_simulation("sumo", (folder+m).replace(".net.xml",".sumo.cfg"), (folder+m), model, m)
        resultados_obtidos[m]["fuzzy"] = start_simulation("sumo", (folder+m).replace(".net.xml",".sumo.cfg"), (folder+m), "fuzzy", m)


        file = open(folder+m.replace(".net.xml",".extras"),"r")
        extras = json.loads(file.read())
        file.close()

        plow(resultados_obtidos[m], extras, m)



if __name__ == '__main__':
    a = "./results/5_10_True_0.1.json"
    main(a)
