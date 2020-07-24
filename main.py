import GA2
import numpy as np
import matplotlib.pyplot as plt
import argparse
import json
import os
import sys
from datetime import datetime
import threading
import socket
import subprocess
import time
from keras.models import Sequential
from keras.layers import Dense


if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Environment variable SUMO_HOME not defined")
import traci



mapas_todos = ["0.net.xml","1.net.xml","2.net.xml","3.net.xml","4.net.xml","5.net.xml","6.net.xml","7.net.xml","8.net.xml","9.net.xml"]


max_speed_caminhao = 30 # ~ 108km/h
max_angle_caminhao = 360 # não sei se é 360 mesmo..
max_dif_altura = 60+10 # +10 margem de segurança





caminho_veiculo = ['A0B0', 'B0C0', 'C0D0', 'D0E0', 'E0F0', 'F0G0', 'G0H0', 'H0I0', 'I0J0', 'J0K0', 'K0L0', 'L0M0', 'M0N0', 'N0O0', 'O0P0', 'P0Q0', 'Q0R0', 'R0S0', 'S0T0']
extras_mapas = None

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
        for m in mapas_todos:
            f = open("./mapas/"+m.replace(".net.xml",".extras"),"r")
            extras_mapas[m] = json.loads(f.read())
            f.close()

    d = extras_mapas[mapa]
    return getClosest(d,len(d),x)


def get_model():
    model = Sequential()
    model.add(Dense(12, activation='sigmoid', input_shape=(6,)))
    model.add(Dense(12, activation='sigmoid'))
    model.add(Dense(12, activation='sigmoid'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer='adam', loss='categorical_crossentropy')

    return model



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

def find_unused_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.bind(('127.0.0.1', 0))
    sock.listen(socket.SOMAXCONN)
    ipaddr, port = sock.getsockname()
    sock.close()

    return port

def terminate_sumo(sumo):

    for _ in range(3):
        if sumo.returncode == None:
            os.system("taskkill.exe /F /im sumo.exe")
            time.sleep(1)




def custom_mutate(genome):
    for i in range(len(genome)):
      for j in range(len(genome[i])):
        genome[i][j] = genome[i][j]*np.random.uniform(low=0.9, high=1.1)

    return genome


def run(model, mapa):

    step = 1
    
    traci.route.add("trip", caminho_veiculo)
    traci.vehicle.add("caminhao", "trip")
    traci.vehicle.setParameter("caminhao","carFollowModel","KraussPS")
    traci.vehicle.setVehicleClass("caminhao","truck")
    traci.vehicle.setShapeClass("caminhao","truck")
    traci.vehicle.setEmissionClass("caminhao","HBEFA3/HDV")
    traci.vehicle.setMaxSpeed("caminhao",max_speed_caminhao) 


    total_fuel = 0

    try:
        while step == 1 or traci.simulation.getMinExpectedNumber() > 0:        
            traci.simulationStep()                          
            vehicles = traci.simulation.getEndingTeleportIDList()        
            for vehicle in vehicles:
                traci.vehicle.remove(vehicle, reason=4)


            try:
                speed = traci.vehicle.getSpeed("caminhao")
                angle = traci.vehicle.getSlope("caminhao")
                x, y, z = traci.vehicle.getPosition3D("caminhao")


                inf10 = get_info_pos(mapa, x+10)
                inf30 = get_info_pos(mapa, x+30)
                inf50 = get_info_pos(mapa, x+50)
                inf70 = get_info_pos(mapa, x+70)

                speed /= max_speed_caminhao
                angle /= max_angle_caminhao
                inf10 = (inf10["z"]-z)/max_dif_altura
                inf30 = (inf30["z"]-z)/max_dif_altura
                inf50 = (inf50["z"]-z)/max_dif_altura
                inf70 = (inf70["z"]-z)/max_dif_altura

                entrada = [speed,angle,inf10,inf30,inf50,inf70]
                # print(entrada)
                r = model.predict(np.array([np.array(entrada)]))[0][0]

                # print("MODEL: ", entrada, r)
                traci.vehicle.setSpeed("caminhao",r*max_speed_caminhao)
                total_fuel += traci.vehicle.getFuelConsumption("caminhao")
            except Exception as e:
                print("######################")
                print(e)
                print("######################")
                pass


            step += 1
    except Exception as e:
        print("######################")
        print(e)
        print("######################")
        raise

    

    time.sleep(1)
    print("Simulation finished")
    traci.close()
    sys.stdout.flush()
    time.sleep(1)

    return total_fuel



def run_pre():

    
    traci.route.add("trip", caminho_veiculo)
    traci.vehicle.add("path_mapper", "trip")
    traci.vehicle.setParameter("path_mapper","carFollowModel","KraussPS")
    traci.vehicle.setVehicleClass("path_mapper","passenger")
    traci.vehicle.setMaxSpeed("path_mapper",1) # ~ 108km/h



    dados = []
    try:
        step = 1
        while step == 1 or traci.simulation.getMinExpectedNumber() > 0:        
            traci.simulationStep()                          
            vehicles = traci.simulation.getEndingTeleportIDList()        
            for vehicle in vehicles:
                traci.vehicle.remove(vehicle, reason=4)

            try:
                traci.vehicle.setSpeed("path_mapper",1)
                angle = traci.vehicle.getSlope("path_mapper")
                x, _, z = traci.vehicle.getPosition3D("path_mapper")

                dados.append({"x":x, "z":z, "angle":angle})
            except:
                pass



            step += 1
    except Exception as e:
        print("######################")
        print(e, step)
        print("######################")

    

    time.sleep(1)
    print("Pre Simulation finished")
    traci.close()
    sys.stdout.flush()
    time.sleep(1)

    return dados


def start_pre_simulation(sumo, scenario, network):
    unused_port_lock = UnusedPortLock()
    unused_port_lock.__enter__()
    remote_port = find_unused_port()

    sumo = subprocess.Popen([sumo, "-c", scenario, "--device.emissions.probability", "1.0", "--remote-port", str(remote_port), "--duration-log.statistics","--log", "logfile.txt"], stdout=sys.stdout, stderr=sys.stderr)    
    unused_port_lock.release()


    try:
        traci.init(remote_port)            
        return run_pre()
    except Exception as e:
        print(e)
        raise
    finally:
        print("Terminating SUMO")  
        terminate_sumo(sumo)
        unused_port_lock.__exit__()

def start_simulation(sumo, scenario, network, output, model, mapa):
    unused_port_lock = UnusedPortLock()
    unused_port_lock.__enter__()
    remote_port = find_unused_port()

    sumo = subprocess.Popen([sumo, "-c", scenario, "--tripinfo-output", output, "--device.emissions.probability", "1.0", "--remote-port", str(remote_port), "--duration-log.statistics","--log", "logfile.txt"], stdout=sys.stdout, stderr=sys.stderr)    
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


def custom_fitness(genome):
    model = get_model()
    model.set_weights(genome)

    mapas = mapas_todos
    folder = "./mapas/"

    consumo_total = 0
    for m in mapas:

        consumo = start_simulation("sumo", (folder+m).replace(".net.xml",".sumo.cfg"), (folder+m), "./output/"+m, model, m)

        consumo_total += consumo

    return 1-(consumo/50000)

def custom_random_genome():
    model = get_model()
    return np.array(model.get_weights())





def pre_simulation():
    mapas = mapas_todos
    folder = "./mapas/"

    for m in mapas:
        dados = start_pre_simulation("sumo", (folder+m).replace(".net.xml",".sumo.cfg"), (folder+m))

        f = open((folder+m).replace(".net.xml",".extras"),"w")
        f.write(json.dumps(dados))
        f.close()

def main():

    pre_simulation()
    return
    population_size   = 10
    iteration_limit   = 10
    cut_half_pop      = True
    replicate_best    = 0.1

    name =  str(population_size)+"_"+\
            str(iteration_limit)+"_"+\
            str(cut_half_pop)+"_"+\
            str(replicate_best)






    g = GA2.GeneticAlgorithm(custom_random_genome)
    g.set_evaluate(custom_fitness)


    g.set_population_size(population_size)
    g.set_iteration_limit(iteration_limit)
    g.set_mutate(custom_mutate)
    g.set_cut_half_population(cut_half_pop)
    g.set_replicate_best(replicate_best)





    g.run()



    infos = {}
    infos["ga_config"] = g.get_config()
    infos["historic"] = g.historic



    f = open("./results/"+name+".json","w")
    f.write(json.dumps(infos, indent=2))
    f.close()



if __name__ == '__main__':
    main()
