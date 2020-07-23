import GA
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
# from ia.model import Model
# import pandas as pd


if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Environment variable SUMO_HOME not defined")
import traci





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




def custom_mutate(index, genome):
    v = genome[i]

    # if np.random.random()>0.5:
    #     v 

def run():

    step = 1
    
    traci.route.add("trip", ['A0B0', 'B0C0', 'C0D0', 'D0E0', 'E0F0', 'F0G0', 'G0H0', 'H0I0', 'I0J0', 'J0K0', 'K0L0', 'L0M0', 'M0N0', 'N0O0', 'O0P0', 'P0Q0', 'Q0R0', 'R0S0', 'S0T0'])
    traci.vehicle.add("caminhao", "trip")
    traci.vehicle.setParameter("caminhao","carFollowModel","KraussPS")
    traci.vehicle.setVehicleClass("caminhao","truck")
    traci.vehicle.setShapeClass("caminhao","truck")
    traci.vehicle.setEmissionClass("caminhao","HBEFA3/HDV")
    traci.vehicle.setMaxSpeed("caminhao",2.2) # aprox 8 km/h


    total_fuel = 0

    try:
        while step == 1 or traci.simulation.getMinExpectedNumber() > 0:        
            traci.simulationStep()                          
            vehicles = traci.simulation.getEndingTeleportIDList()        
            for vehicle in vehicles:
                traci.vehicle.remove(vehicle, reason=4)

            # print("getAccel",traci.vehicle.getAccel("caminhao"))
            # print("getVehicleClass",traci.vehicle.getVehicleClass("caminhao"))
            # print("getEmissionClass",traci.vehicle.getEmissionClass("caminhao"))
            # print("getFuelConsumption",traci.vehicle.getFuelConsumption("caminhao"))

            try:
                total_fuel += traci.vehicle.getFuelConsumption("caminhao")
            except:
                pass

            step += 1
    except Exception as e:
        print("######################")
        print(e)
        print("######################")

    

    time.sleep(1)
    print("Simulation finished")
    traci.close()
    sys.stdout.flush()
    time.sleep(1)

    return total_fuel

def start_simulation(sumo, scenario, network, output):
    unused_port_lock = UnusedPortLock()
    unused_port_lock.__enter__()
    remote_port = find_unused_port()

    sumo = subprocess.Popen([sumo, "-c", scenario, "--tripinfo-output", output, "--device.emissions.probability", "1.0", "--remote-port", str(remote_port), "--duration-log.statistics","--log", "logfile.txt"], stdout=sys.stdout, stderr=sys.stderr)    
    unused_port_lock.release()


    try:
        traci.init(remote_port)            
        return run()
    except Exception as e:
        print(e)
        # terminate_sumo(sumo)
        # unused_port_lock.__exit__()
        raise
    finally:
        print("Terminating SUMO")  
        terminate_sumo(sumo)
        unused_port_lock.__exit__()


def custom_fitness():

    mapas = ["0.net.xml","1.net.xml","2.net.xml","3.net.xml","4.net.xml","5.net.xml","6.net.xml","7.net.xml","8.net.xml","9.net.xml"]
    folder = "./mapas/"

    consumo_total = 0
    for m in mapas:

        consumo = start_simulation("sumo", (folder+m).replace(".net.xml",".sumo.cfg"), (folder+m), "./output/"+m)

        consumo_total += consumo

    return 1-(consumo/50000)


def main():

    custom_fitness()
    return
    population_size   = 10
    iteration_limit   = 10
    crossover_type    = 3
    crossover_rate    = 0.8
    mutation_rate     = 0.5
    cut_half_pop      = True
    replicate_best    = 0.1

    name =  str(population_size)+"_"+\
            str(iteration_limit)+"_"+\
            str(crossover_type)+"_"+\
            str(crossover_rate)+"_"+\
            str(mutation_rate)+"_"+\
            str(cut_half_pop)+"_"+\
            str(replicate_best)




    # df = pd.read_csv(args.dataset[0])

    # model = Model()
    # df = model.make_fair(df, dataset_name)

    # target = targets[dataset_name]
    # target = df.pop(target)


    def custom_random_genome():
        return np.random.random(20)

    g = GA.GeneticAlgorithm(custom_random_genome)
    g.set_evaluate(custom_fitness)


    g.set_population_size(population_size)
    g.set_iteration_limit(iteration_limit)
    g.set_crossover_type(crossover_type)
    g.set_crossover_rate(crossover_rate)
    g.set_mutate(custom_mutate)
    g.set_mutation_rate(mutation_rate)
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
