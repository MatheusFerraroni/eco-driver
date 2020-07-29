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

caminho_veiculo = ['A0B0', 'B0C0', 'C0D0', 'D0E0', 'E0F0', 'F0G0', 'G0H0', 'H0I0', 'I0J0', 'J0K0', 'K0L0', 'L0M0', 'M0N0', 'N0O0', 'O0P0', 'P0Q0', 'Q0R0', 'R0S0', 'S0T0']


if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Environment variable SUMO_HOME not defined")
import traci

def get_model():
    model = Sequential()
    model.add(Dense(8, activation='sigmoid', input_shape=(6,)))
    model.add(Dense(8, activation='sigmoid'))
    model.add(Dense(8, activation='sigmoid'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer='adam', loss='categorical_crossentropy')

    return model


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

    step = 1
    
    traci.route.add("trip", caminho_veiculo)
    traci.vehicle.add("caminhao", "trip")
    traci.vehicle.setParameter("caminhao","carFollowModel","KraussPS")
    traci.vehicle.setVehicleClass("caminhao","truck")
    traci.vehicle.setShapeClass("caminhao","truck")
    traci.vehicle.setEmissionClass("caminhao","HBEFA3/HDV")
    traci.vehicle.setMaxSpeed("caminhao",max_speed_caminhao) 
    r = 1

    total_fuel = 0

    try:
        while step == 1 or traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()


            try:
                speed = traci.vehicle.getSpeed("caminhao")
                angle = traci.vehicle.getSlope("caminhao")
                x, y, z = traci.vehicle.getPosition3D("caminhao")


                inf10 = get_info_pos(mapa, x+10)
                inf30 = get_info_pos(mapa, x+30)
                inf50 = get_info_pos(mapa, x+50)
                inf70 = get_info_pos(mapa, x+70)



                if model!=None:
                    speed /= max_speed_caminhao
                    angle /= 90
                    inf10 = inf10["angle"]/90
                    inf30 = inf30["angle"]/90
                    inf50 = inf50["angle"]/90
                    inf70 = inf70["angle"]/90
                    entrada = [speed, angle, inf10, inf30, inf50, inf70]

                    r = model.predict(np.array([np.array(entrada)]))[0][0]
                    
                    if r==0:
                        r = 0.01
                    traci.vehicle.setSpeed("caminhao",r*max_speed_caminhao)
                total_fuel += traci.vehicle.getFuelConsumption("caminhao")
            except Exception as e:
                pass


            step += 1
    except Exception as e:
        print("######################")
        print(e)
        print("######################")
        raise



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

def main():
    f = open("./results/20_20_True_0.1.json","r")
    dado = json.loads(f.read())
    f.close()
    gen = dado["historic"][-1]["best_genome"]
    gen = converter(gen)
    model = get_model()
    model.set_weights(gen)

    folder = "./mapas_validation/"
    mapas = os.listdir(folder)

    mapas = [mapa for mapa in mapas if mapa.split(".")[-1]=="xml" and mapa.split(".")[-2]=="net"]
    
    for m in mapas:
        dados = start_simulation("sumo", (folder+m).replace(".net.xml",".sumo.cfg"), (folder+m), None, m)
        dados = start_simulation("sumo", (folder+m).replace(".net.xml",".sumo.cfg"), (folder+m), model, m)


if __name__ == '__main__':
    main()
