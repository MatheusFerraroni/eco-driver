import GA
import numpy as np
import matplotlib.pyplot as plt
import argparse
import json
import os
import sys
from datetime import datetime
import threading

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
    if sumo.returncode == None:
        # os.kill(sumo.pid, signal.SIGILL)
        os.system("taskkill.exe /F /im sumo.exe")
        time.sleep(1)
        # if sumo.returncode == None:
        #     os.kill(sumo.pid, signal.SIGKILL)
        #     time.sleep(1)
        #     if sumo.returncode == None:
        #         time.sleep(10)




def custom_mutate(index, genome):
    if genome[index]==0:
        genome[index] = 1
    else:
        genome[index] = 0
    return genome




# def run(network, begin, end, interval, config_file, versao_i):

#     step = 1

#     controlador = Trabalho(config_file, versao_i)

#     while step == 1 or traci.simulation.getMinExpectedNumber() > 0:
#         traci.simulationStep()

#         vehicles = traci.simulation.getEndingTeleportIDList()
#         for vehicle in vehicles:
#             traci.vehicle.remove(vehicle, reason=4)

#         controlador.do_work(traci, step) # magic is here

#         step += 1

#     controlador.stop()

#     time.sleep(3)
#     print("Simulation finished")
#     traci.close()
#     sys.stdout.flush()
#     time.sleep(3)


# def start_simulation(scenario, network, begin, end, interval, output, config_file, versao_i):
#     unused_port_lock = UnusedPortLock()
#     unused_port_lock.__enter__()
#     remote_port = find_unused_port()

#     sumo = subprocess.Popen(["sumo-gui", "-c", scenario, "--tripinfo-output", output, "--device.emissions.probability", "1.0", "--remote-port", str(remote_port)], stdout=sys.stdout, stderr=sys.stderr)
#     unused_port_lock.release()

#     try:
#         traci.init(remote_port)
#         run(network, begin, end, interval, config_file, versao_i)
#     except Exception as e:
#         print(e)
#         raise
#     finally:
#         print("Terminating SUMO")
#         terminate_sumo(sumo)
#         unused_port_lock.__exit__()



def main():

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


    def custom_fitness(genome):
        return np.random.random()
        # bool_genome = list(map(bool, genome))
        # return model.evaluate(df.loc[:, bool_genome].copy(), target)

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













# from __future__ import division
# import os
# import sys
# import subprocess
# import signal
# import socket
# import threading
# import time
# from optparse import OptionParser
# import Simulation

# if 'SUMO_HOME' in os.environ:
#     tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
#     sys.path.append(tools)
# else:
#     sys.exit("Environment variable SUMO_HOME not defined")

# sys.path.append(os.path.join('/home/-/sumo-1.5.0/tools'))

# import traci

# class UnusedPortLock:
#     lock = threading.Lock()

#     def __init__(self):
#         self.acquired = False

#     def __enter__(self):
#         self.acquire()

#     def __exit__(self):
#         self.release()

#     def acquire(self):
#         if not self.acquired:
#             UnusedPortLock.lock.acquire()
#             self.acquired = True

#     def release(self):
#         if self.acquired:
#             UnusedPortLock.lock.release()
#             self.acquired = False

# def find_unused_port():
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
#     sock.bind(('127.0.0.1', 0))
#     sock.listen(socket.SOMAXCONN)
#     ipaddr, port = sock.getsockname()
#     sock.close()
#     return port

# def terminate_sumo(sumo):
#     if sumo.returncode == None:
#         os.kill(sumo.pid, signal.SIGILL)
#         time.sleep(0.5)
#         if sumo.returncode == None:
#             os.kill(sumo.pid, signal.SIGKILL)
#             time.sleep(1)
#             if sumo.returncode == None:
#                 time.sleep(10)


# def run(network, begin, end, interval):

#     step = 1
    
#     adition = Simulation.Vehicles.add1(traci)    
    
#     while step == 1 or traci.simulation.getMinExpectedNumber() > 0:        
#         traci.simulationStep()                          
#         vehicles = traci.simulation.getEndingTeleportIDList()        
#         for vehicle in vehicles:
#             traci.vehicle.remove(vehicle, reason=4)    

#         step += 1
    
#     time.sleep(10)
#     print("Simulation finished")
#     traci.close()
#     sys.stdout.flush()
#     time.sleep(10)
        
# def start_simulation(sumo, scenario, network, begin, end, interval, output):
#     unused_port_lock = UnusedPortLock()
#     unused_port_lock.__enter__()
#     remote_port = find_unused_port()

#     sumo = subprocess.Popen([sumo, "-c", scenario, "--tripinfo-output", output, "--device.emissions.probability", "1.0", "--remote-port", str(remote_port), "--duration-log.statistics","--log", "logfile.txt"], stdout=sys.stdout, stderr=sys.stderr)    
#     unused_port_lock.release()


#     try:
#         traci.init(remote_port)            
#         run(network, begin, end, interval)
#     except Exception as e:
#         print(e)        
#         raise
#     finally:
#         print("Terminating SUMO")  
#         terminate_sumo(sumo)
#         unused_port_lock.__exit__()
        
# def main():

#     parser = OptionParser()
#     parser.add_option("-c", "--command", dest="command", default="sumo-gui", help="The command used to run SUMO [default: %default]", metavar="COMMAND")
#     parser.add_option("-s", "--scenario", dest="scenario", default="map.sumocfg", help="A SUMO configuration file [default: %default]", metavar="FILE")
#     parser.add_option("-n", "--network", dest="network", default="map.net.xml", help="A SUMO network definition file [default: %default]", metavar="FILE")    
#     parser.add_option("-b", "--begin", dest="begin", type="int", default=0, action="store", help="The simulation time (s) at which the re-routing begins [default: %default]", metavar="BEGIN")
#     parser.add_option("-e", "--end", dest="end", type="int", default=600, action="store", help="The simulation time (s) at which the re-routing ends [default: %default]", metavar="END")
#     parser.add_option("-i", "--interval", dest="interval", type="int", default=1, action="store", help="The interval (s) of classification [default: %default]", metavar="INTERVAL")    
#     parser.add_option("-o", "--full-output", dest="output", default="output1.xml", help="The XML file at which the output must be written [default: %default]", metavar="FILE")


#     (options, args) = parser.parse_args()
    

        
#     start_simulation(options.command, options.scenario, options.network, options.begin, options.end, options.interval, options.output)


# if __name__ == "__main__":
#     main()










# class Vehicles:

#     def add1(traci):
#         traci.route.add("trip", ['3to4', '4to5', '5to6', '6to7', '7to8', '8to9', '9to10', '10to11', '11to12', '12to13', '13to14', '14to15', '15to16', '16to17', '17to18', '18to19', '19to20', '20to21', '21to22', '22to25'])
#         traci.vehicle.add("caminhao", "trip")
#         traci.vehicle.setParameter("caminhao","carFollowModel","KraussPS")
#         traci.vehicle.setVehicleClass("caminhao","truck")
#         traci.vehicle.setShapeClass("caminhao","truck")
#         traci.vehicle.setEmissionClass("caminhao","HBEFA3/HDV")
#         traci.vehicle.setMaxSpeed("caminhao",2.2) # aprox 8 km/h 
#         print(traci.vehicle.getAccel("caminhao"))
#         print(traci.vehicle.getVehicleClass("caminhao"))    
#         print(traci.vehicle.getEmissionClass("caminhao"))       

#         traci.vehicle.add("carrinheiro", "trip")        
#         traci.vehicle.setVehicleClass("carrinheiro","pedestrian")
#         traci.vehicle.setShapeClass("carrinheiro","pedestrian")
#         traci.vehicle.setMaxSpeed("carrinheiro",1) # aprox 4 km/h
#         traci.vehicle.setEmissionClass("carrinheiro","Zero")
        
#         return True
