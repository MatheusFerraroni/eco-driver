import GA2
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

    if sumo.returncode == None:
        os.system("taskkill.exe /F /im sumo.exe")
        time.sleep(1)




def run(mapa, v):

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
                # print(v,speed)
                angle = traci.vehicle.getSlope("caminhao")
                x, y, z = traci.vehicle.getPosition3D("caminhao")
                total_fuel += traci.vehicle.getFuelConsumption("caminhao")


                # traci.vehicle.setSpeed("caminhao",v)

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

    

    print("Simulation finished")
    traci.close()
    sys.stdout.flush()
    time.sleep(1)
    return total_fuel





def start_simulation(sumo, scenario, network, output, mapa, v):
    unused_port_lock = UnusedPortLock()
    unused_port_lock.__enter__()
    remote_port = find_unused_port()

    sumo = subprocess.Popen([sumo, "-c", scenario, "--tripinfo-output", output, "--device.emissions.probability", "1.0", "--remote-port", str(remote_port), "--duration-log.statistics","--log", "logfile.txt"], stdout=sys.stdout, stderr=sys.stderr)    
    unused_port_lock.release()


    try:
        traci.init(remote_port)            
        return run(mapa, v)
    except Exception as e:
        print(e)
        raise
    finally:
        print("Terminating SUMO")  
        terminate_sumo(sumo)
        unused_port_lock.__exit__()











def main():

    mapas = mapas_todos
    folder = "./mapas/"

    for m in mapas:
        v = 0
        # for v in range(3,30,3):

        vtxt = 'dft'
            # if v<10:
            #     vtxt = "0"+str(v)
            # else:
            #     vtxt = str(v)
        start_simulation("sumo", (folder+m).replace(".net.xml",".sumo.cfg"), (folder+m), "./output_fixed/"+m+"_vel("+str(vtxt)+")"+".xml", m, v)




if __name__ == '__main__':
    main()
