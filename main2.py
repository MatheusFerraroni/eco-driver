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
import math
from random import gauss
import ConsuptionModel as cM


if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Environment variable SUMO_HOME not defined")
import traci



mapas_todos = [
"super.net.xml",
]

max_speed_caminhao = 30 # ~ 108km/h
extras_mapas = None





caminho_veiculo = ['AA0AB0','AB0AC0','AC0AD0','AD0AE0','AE0AF0','AF0AG0','AG0AH0','AH0AI0','AI0AJ0','AJ0AK0','AK0AL0','AL0AM0','AM0AN0','AN0AO0',
'AO0AP0','AP0AQ0','AQ0AR0','AR0AS0','AS0AT0','AT0AU0','AU0AV0','AV0AW0','AW0AX0','AX0AY0','AY0AZ0','AZ0BA0','BA0BB0','BB0BC0','BC0BD0','BD0BE0',
'BE0BF0','BF0BG0','BG0BH0','BH0BI0','BI0BJ0','BJ0BK0','BK0BL0','BL0BM0','BM0BN0','BN0BO0','BO0BP0','BP0BQ0','BQ0BR0','BR0BS0','BS0BT0','BT0BU0',
'BU0BV0','BV0BW0','BW0BX0','BX0BY0','BY0BZ0','BZ0CA0','CA0CB0','CB0CC0','CC0CD0','CD0CE0','CE0CF0','CF0CG0','CG0CH0','CH0CI0','CI0CJ0','CJ0CK0',
'CK0CL0','CL0CM0','CM0CN0','CN0CO0','CO0CP0','CP0CQ0','CQ0CR0','CR0CS0','CS0CT0','CT0CU0','CU0CV0','CV0CW0','CW0CX0','CX0CY0','CY0CZ0','CZ0DA0',
'DA0DB0','DB0DC0','DC0DD0','DD0DE0','DE0DF0','DF0DG0','DG0DH0','DH0DI0','DI0DJ0','DJ0DK0','DK0DL0','DL0DM0','DM0DN0','DN0DO0','DO0DP0','DP0DQ0',
'DQ0DR0','DR0DS0','DS0DT0','DT0DU0','DU0DV0','DV0DW0','DW0DX0','DX0DY0','DY0DZ0','DZ0EA0','EA0EB0','EB0EC0','EC0ED0',
'ED0EE0','EE0EF0','EF0EG0','EG0EH0','EH0EI0','EI0EJ0','EJ0EK0','EK0EL0','EL0EM0','EM0EN0','EN0EO0','EO0EP0','EP0EQ0',
'EQ0ER0','ER0ES0','ES0ET0','ET0EU0','EU0EV0','EV0EW0','EW0EX0','EX0EY0','EY0EZ0','EZ0FA0','FA0FB0','FB0FC0','FC0FD0',
'FD0FE0','FE0FF0','FF0FG0','FG0FH0','FH0FI0','FI0FJ0','FJ0FK0','FK0FL0','FL0FM0','FM0FN0','FN0FO0','FO0FP0','FP0FQ0',
'FQ0FR0','FR0FS0','FS0FT0','FT0FU0','FU0FV0','FV0FW0','FW0FX0','FX0FY0','FY0FZ0','FZ0GA0','GA0GB0','GB0GC0','GC0GD0','GD0GE0',
'GE0GF0','GF0GG0','GG0GH0','GH0GI0','GI0GJ0','GJ0GK0','GK0GL0','GL0GM0','GM0GN0','GN0GO0','GO0GP0','GP0GQ0','GQ0GR0','GR0GS0',
'GS0GT0','GT0GU0','GU0GV0','GV0GW0','GW0GX0','GX0GY0','GY0GZ0','GZ0HA0','HA0HB0','HB0HC0','HC0HD0','HD0HE0','HE0HF0','HF0HG0',
'HG0HH0','HH0HI0','HI0HJ0','HJ0HK0','HK0HL0','HL0HM0','HM0HN0','HN0HO0','HO0HP0','HP0HQ0','HQ0HR0','HR0HS0','HS0HT0','HT0HU0',
'HU0HV0','HV0HW0','HW0HX0','HX0HY0','HY0HZ0','HZ0IA0','IA0IB0','IB0IC0','IC0ID0','ID0IE0','IE0IF0','IF0IG0','IG0IH0','IH0II0',
'II0IJ0','IJ0IK0','IK0IL0','IL0IM0','IM0IN0','IN0IO0','IO0IP0','IP0IQ0','IQ0IR0','IR0IS0','IS0IT0','IT0IU0','IU0IV0','IV0IW0',
'IW0IX0','IX0IY0','IY0IZ0','IZ0JA0','JA0JB0','JB0JC0','JC0JD0','JD0JE0','JE0JF0','JF0JG0','JG0JH0','JH0JI0','JI0JJ0','JJ0JK0',
'JK0JL0','JL0JM0','JM0JN0','JN0JO0','JO0JP0','JP0JQ0','JQ0JR0','JR0JS0','JS0JT0','JT0JU0','JU0JV0','JV0JW0','JW0JX0','JX0JY0',
'JY0JZ0','JZ0KA0','KA0KB0','KB0KC0','KC0KD0','KD0KE0','KE0KF0','KF0KG0','KG0KH0','KH0KI0','KI0KJ0','KJ0KK0','KK0KL0','KL0KM0',
'KM0KN0','KN0KO0','KO0KP0','KP0KQ0','KQ0KR0','KR0KS0','KS0KT0','KT0KU0','KU0KV0','KV0KW0','KW0KX0','KX0KY0','KY0KZ0','KZ0LA0',
'LA0LB0','LB0LC0','LC0LD0','LD0LE0','LE0LF0','LF0LG0','LG0LH0','LH0LI0','LI0LJ0','LJ0LK0','LK0LL0','LL0LM0','LM0LN0','LN0LO0',
]

def calculate_real_fuel(speed,accel,slope,instant_fuel):
    modelo = cM.ModelConsuption(speed, accel, slope)
    consuption = modelo.run()
    instant_fuel = consuption
    
    return instant_fuel

def calculate_power(slope,speed):
    # slope : angulo em graus
	# velocidade : m/s
	accelG = 10 # m/s^2
	coefAtrito = 0.2
	massa = 1000 # kg
	rendimento = 0.85
	angulo = math.radians(slope) # graus para radianos
	seno = math.sin(angulo)
	cosseno = math.cos(angulo)

	F1 = massa * accelG * seno # Forca 1
	Fat = coefAtrito * (massa * accelG * cosseno) # Forca atrito

	Fmotor = F1 + Fat # Forca do motor

	deslocamento = ((seno ** 2) + (cosseno ** 2)) ** 1/2

	trabalho = Fmotor * deslocamento

	potencia = (Fmotor * velocidade)/rendimento

	return potencia

def calculate_new_fuel(instant_fuel, instant_slope, max_slope, instant_acell, max_accel):


    total_accel = instant_acell/max_accel
    total_slope = instant_slope/max_slope

    if total_slope>=0 and total_accel>=0:
        instant_fuel += total_slope*4

    return instant_fuel

def get_model():
    model = Sequential()
    model.add(Dense(16, input_shape=(8,)))
    model.add(Dense(24))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer='adam', loss='mean_squared_error')

    return model


# def returnScaledOutput(youtput):
#   yscaled = youtput + 0.25
#   return min(yscaled, 1.0)


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
    if sumo.returncode != None:
        os.system("taskkill.exe /F /im sumo.exe")
        time.sleep(1)


def norm_force(a):
    a = min(a,1)
    a = max(a,-1)
    return a



# def returnRandomWeightVariation(wei):
#     updated_weight = gauss(wei, 0.05)
#     if updated_weight < -1:
#         return -1
#     if updated_weight > 1:
#         return 1
#     return updated_weight



def gaus(ger):
    return 0.1+0.9*math.pow(math.e,(-math.pow((2*ger),4)))


def custom_mutate(wei, progresso):
    if type(wei)==np.ndarray:
        ret = []
        for w in wei:
            ret.append(custom_mutate(w,progresso))
        return np.array(ret, dtype=object)


    if np.random.random() < 0.2*gaus(progresso):
        return np.random.uniform(low=-1, high=1)
    else:
        return norm_force(wei + np.random.uniform(low=-0.2, high=0.2)*gaus(progresso))



def run(model, mapa):


    traci.route.add("trip", caminho_veiculo)
    traci.vehicle.add("caminhao", "trip")
    traci.vehicle.setParameter("caminhao","carFollowModel","KraussPS")
    traci.vehicle.setVehicleClass("caminhao","truck")
    traci.vehicle.setShapeClass("caminhao","truck")
    traci.vehicle.setEmissionClass("caminhao","PHEMlight/PC_G_EU4")
    traci.vehicle.setMaxSpeed("caminhao",max_speed_caminhao)
    r = 1
    step = 1
    total_fuel = 0
    max_angulo = 60

    last_speed = 0
    try:
        while step == 1 or traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()


            try:
                speed = traci.vehicle.getSpeed("caminhao")
                angle = traci.vehicle.getSlope("caminhao")
                x, y, z = traci.vehicle.getPosition3D("caminhao")

                max_acel = traci.vehicle.getAccel("caminhao")
                inst_acel = traci.vehicle.getAcceleration("caminhao")

                inf10 = get_info_pos(mapa,  x+10)
                inf20 = get_info_pos(mapa,  x+20)
                inf30 = get_info_pos(mapa,  x+30)
                inf40 = get_info_pos(mapa,  x+40)
                inf50 = get_info_pos(mapa,  x+50)
                # inf60 = get_info_pos(mapa,  x+60)
                # inf70 = get_info_pos(mapa,  x+70)
                # inf100 = get_info_pos(mapa, x+100)

                inf10 = inf10["angle"]/max_angulo
                inf20 = inf20["angle"]/max_angulo
                inf30 = inf30["angle"]/max_angulo
                inf40 = inf40["angle"]/max_angulo
                inf50 = inf50["angle"]/max_angulo
                # inf60 = inf60["angle"]/max_angulo
                # inf70 = inf70["angle"]/max_angulo
                # inf100 = inf100["angle"]/max_angulo

                entrada = [speed/max_speed_caminhao, last_speed, angle/max_angulo, inf10, inf20, inf30, inf40, inf50]


                r = model.predict(np.array([np.array(entrada)]))[0][0]
                last_speed = r




                if r<0.1:
                    r = 0.1
                # print(r, max_speed_caminhao , r*max_speed_caminhao)
                traci.vehicle.setSpeed("caminhao",r*max_speed_caminhao)
                instant_fuel_consuption = traci.vehicle.getFuelConsumption("caminhao")

                # instant_fuel_consuption2 = calculate_new_fuel(instant_fuel_consuption, angle, max_angulo, inst_acel, max_acel)
                instant_fuel_consuption2 = calculate_real_fuel(speed, accel,slope,instant_fuel)

                total_fuel += instant_fuel_consuption2
            except Exception as e:
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
    # time.sleep(1)

    return total_fuel



def run_pre():

    caminho_veiculo_pre = [
'AA0AB0','AB0AC0','AC0AD0','AD0AE0','AE0AF0','AF0AG0','AG0AH0','AH0AI0','AI0AJ0','AJ0AK0','AK0AL0','AL0AM0','AM0AN0','AN0AO0',
'AO0AP0','AP0AQ0','AQ0AR0','AR0AS0','AS0AT0','AT0AU0','AU0AV0','AV0AW0','AW0AX0','AX0AY0','AY0AZ0','AZ0BA0','BA0BB0','BB0BC0','BC0BD0','BD0BE0',
'BE0BF0','BF0BG0','BG0BH0','BH0BI0','BI0BJ0','BJ0BK0','BK0BL0','BL0BM0','BM0BN0','BN0BO0'
    ]
    
    # caminho_veiculo_pre = caminho_veiculo
    traci.route.add("trip", caminho_veiculo_pre)
    traci.vehicle.add("path_mapper", "trip")
    traci.vehicle.setParameter("path_mapper","carFollowModel","KraussPS")
    traci.vehicle.setVehicleClass("path_mapper","passenger")
    traci.vehicle.setMaxSpeed("path_mapper",0.3) # 3.6



    dados = []
    try:
        step = 1
        while step == 1 or traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()

            try:
                traci.vehicle.setSpeed("path_mapper",0.3)
                angle = traci.vehicle.getSlope("path_mapper")
                x, _, z = traci.vehicle.getPosition3D("path_mapper")
                speed = traci.vehicle.getSpeed("path_mapper")


                dados.append({"x":x, "z":z, "angle":angle})
            except:
                pass



            step += 1
    except Exception as e:
        print("######################")
        print(e, step)
        print("######################")



    # time.sleep(1)
    print("Pre Simulation finished")
    traci.close()
    sys.stdout.flush()
    # time.sleep(1)

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


def custom_fitness(genome, outputfile):
    model = get_model()

    model.set_weights(genome)

    mapas = mapas_todos
    folder = "./mapas/"

    consumo_total = 0
    for m in mapas:

        consumo = start_simulation("sumo", (folder+m).replace(".net.xml",".sumo.cfg"), (folder+m), "./output/"+m+outputfile, model, m)

        consumo_total += consumo

        # if consumo_total==float("Infinity"): # isso faz pular mapas no teste caso a gente ja tenha identificado algum muito lento
        #     break


    f = open("./output/"+m+outputfile,"r")
    conteudo = f.read()
    f.close()
    conteudo = conteudo.split("\n")
    conteudo[33] = conteudo[33].split("fuel_abs")
    conteudo[33] = conteudo[33][0]+"fuel_abs=\"{:.6f}\" electricity_abs=\"0\"/>".format(consumo_total)
    conteudo = "\n".join(conteudo)
    f = open("./output/"+m+outputfile,"w")
    f.write(conteudo)
    f.close()


    return 1/consumo_total

def custom_random_genome():
    model = get_model()

    w = model.get_weights()

    return custom_mutate(np.array(w, dtype=object), 0)





def pre_simulation():

    mapas = [
        # "super.net.xml",
        "0.net.xml",
        "1.net.xml",
        "2.net.xml",
        "3.net.xml",
        "4.net.xml",
        "5.net.xml",
        "6.net.xml",
        "7.net.xml",
        "8.net.xml",
        "9.net.xml",
        "10.net.xml",
        "11.net.xml",
        "12.net.xml",
        "13.net.xml",
        "14.net.xml",
        "15.net.xml",
        "16.net.xml",
        "17.net.xml",
        "18.net.xml",
        "19.net.xml",
        "20.net.xml",
        "21.net.xml",
        "22.net.xml",
        "23.net.xml",
        "24.net.xml",
        "25.net.xml",
        "26.net.xml",
        "27.net.xml",
        "28.net.xml",
        "29.net.xml",
    ]
    folder = "./mapas_validation/"

    for m in mapas:
        dados = start_pre_simulation("sumo", (folder+m).replace(".net.xml",".sumo.cfg"), (folder+m))

        f = open((folder+m).replace(".net.xml",".extras"),"w")
        f.write(json.dumps(dados))
        f.close()



def main():



    folder = './output/'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


    pre_simulation()
    return
    population_size   = 10
    iteration_limit   = 11
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
    g.set_stop_criteria_type(1)
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
