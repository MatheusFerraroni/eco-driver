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
import fuzzy_in_four
import ConsuptionModel as cM
import math

caminho_veiculo = [
'AA0AB0','AB0AC0','AC0AD0','AD0AE0','AE0AF0','AF0AG0','AG0AH0','AH0AI0','AI0AJ0','AJ0AK0','AK0AL0','AL0AM0','AM0AN0','AN0AO0',
'AO0AP0','AP0AQ0','AQ0AR0','AR0AS0','AS0AT0','AT0AU0','AU0AV0','AV0AW0','AW0AX0','AX0AY0','AY0AZ0','AZ0BA0','BA0BB0','BB0BC0','BC0BD0','BD0BE0',
'BE0BF0','BF0BG0','BG0BH0','BH0BI0','BI0BJ0','BJ0BK0','BK0BL0','BL0BM0','BM0BN0','BN0BO0','BO0BP0', 'BP0BQ0', 'BQ0BR0', 'BR0BS0', 'BS0BT0','BT0BU0','BU0BV0','BV0BW0', 'BW0BX0', 'BX0BY0'
    ]

caminho_veiculo_super = ['AA0AB0','AB0AC0','AC0AD0','AD0AE0','AE0AF0','AF0AG0','AG0AH0','AH0AI0','AI0AJ0','AJ0AK0','AK0AL0','AL0AM0','AM0AN0','AN0AO0',
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

max_speed_caminhao = 30 # ~ 108km/h
max_dif_altura = 50
extras_mapas = None
z_add = 30


sim_atual = 0

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Environment variable SUMO_HOME not defined")
import traci

def get_model():
    model = Sequential()
    model.add(Dense(16, input_shape=(8,)))
    model.add(Dense(24))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer='adam', loss='mean_squared_error')

    return model

def calculate_real_fuel(speed,accel,slope,instant_fuel):
    modelo = cM.ModelConsuption(speed, accel, slope)
    consuption = modelo.run()
    instant_fuel = consuption
    
    return instant_fuel


def calculate_real_fuel2(speed,accel,slope,instant_fuel):
    modelo = cM.ModelConsuption(speed, accel, slope)
    consuption = modelo.run()
    p = 0.1 # Percentage increase in consumption [0,1]
    factor_RPM = ((speed**2)*(p))/(30**2)
    instant_fuel = consuption + consuption*factor_RPM
   
    return instant_fuel

def calculate_real_fuel3(speed,accel,slope,instant_fuel):
    modelo = cM.ModelConsuption(speed, accel, slope)
    consuption = modelo.run()
    p = 0.1 # Percentage increase in consumption [0,1]
    factor_RPM = (math.exp(speed)*p)/(math.exp(30))
    instant_fuel = consuption + consuption*factor_RPM
   
    return instant_fuel

def calculate_real_fuel4(speed,accel,slope,instant_fuel):
    modelo = cM.ModelConsuption(speed, accel, slope)
    consuption = modelo.run()
    p = 0.2 # Percentage increase in consumption [0,1]
    maxSlope = 25
    maxSpeed = 30
    factor_Slope = math.exp(slope)/math.exp(maxSlope)
    factor_Speed = math.exp(speed)/math.exp(maxSpeed)
    factor_RPM = factor_Speed*factor_Speed*p
    instant_fuel = consuption + consuption*factor_RPM
   
    return instant_fuel


def calculate_new_fuel(instant_fuel, instant_slope, max_slope, instant_acell, max_accel):


    total_accel = instant_acell/max_accel
    total_slope = instant_slope/max_slope

    if total_slope>=0 and total_accel>=0:
        instant_fuel += total_slope*4

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
        # folder = "./mapas_validation/"
        folder = "./mapas/"
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
    global sim_atual
    npdf = 0
    mean_speed = 0
    pdf = np.zeros((110,), dtype=float)

    f_2 = fuzzy_in_two.Algorithm()
    f_4 = fuzzy_in_four.Algorithm()

    step = 0

    traci.route.add("trip", caminho_veiculo_super)
    traci.vehicle.add("caminhao", "trip")
    if type(model)==str and model!="Fuzzy" and model!="Fuzzy2":
        traci.vehicle.setParameter("caminhao","carFollowModel",model)
        print("entrou",model)
    else:
        traci.vehicle.setParameter("caminhao","carFollowModel","KraussPS")
        print("padrao")
    traci.vehicle.setVehicleClass("caminhao","truck")
    traci.vehicle.setShapeClass("caminhao","truck")
    traci.vehicle.setEmissionClass("caminhao","PHEMlight/PC_G_EU4")
    traci.vehicle.setMaxSpeed("caminhao",max_speed_caminhao) 

    r = 1
    max_angulo = 60

    total_fuel = 0
    last_speed = 0

    mean_speed = 0
    mean_fuel_second = 0

    dados_retorno = []



    try:
        while step == 0 or traci.simulation.getMinExpectedNumber() > 0:
            if(step%100==0):
                print(step)

            traci.simulationStep()
            step += 1

            try:
                speed = traci.vehicle.getSpeed("caminhao")
                mean_speed += speed
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


                i_pdf =  int(speed*3.6+0.49)
                pdf[i_pdf] += 1
                npdf += 1


                if type(model)!=str and model!="fuzzy":

                    inf10 = inf10["angle"]/max_angulo
                    inf20 = inf20["angle"]/max_angulo
                    inf30 = inf30["angle"]/max_angulo
                    inf40 = inf40["angle"]/max_angulo
                    inf50 = inf50["angle"]/max_angulo
                    inf60 = inf60["angle"]/max_angulo
                    inf70 = inf70["angle"]/max_angulo
                    inf100 = inf100["angle"]/max_angulo


                    entrada = [speed/max_speed_caminhao, last_speed, angle/max_angulo, inf10, inf20, inf30, inf40, inf50]


                    r = model.predict(np.array([np.array(entrada)]))[0][0]
                    last_speed = r




                    if r<0.1:
                        r = 0.1
                    traci.vehicle.setSpeed("caminhao",r*max_speed_caminhao)
                elif model=="fuzzy":
                    normalization = 1 #90
                    inf10 = inf10["angle"]/normalization
                    inf30 = inf30["angle"]/normalization
                    inf50 = inf50["angle"]/normalization
                    inf70 = inf70["angle"]/normalization

                    # FUZZY
                    r = f_2.findSpeed(speed,angle/normalization, inf10, inf30, inf50, inf70)

                    traci.vehicle.setSpeed("caminhao",r)

                elif model=="fuzzy2":
                    normalization = 1 #90
                    inf10 = inf10["angle"]/normalization
                    inf30 = inf30["angle"]/normalization
                    inf50 = inf50["angle"]/normalization
                    inf70 = inf70["angle"]/normalization

                    # FUZZY
                    r = f_4.findSpeed(speed,angle/normalization, inf10, inf30, inf50, inf70)

                    traci.vehicle.setSpeed("caminhao",r)

                fuel_last_step = traci.vehicle.getFuelConsumption("caminhao")
                #instant_fuel_consuption2 = calculate_new_fuel(fuel_last_step, angle, max_angulo, inst_acel, max_acel)
                instant_fuel_consuption2 = calculate_real_fuel4(speed, inst_acel, angle, fuel_last_step)

                total_fuel += instant_fuel_consuption2

                dados_retorno.append({
                    "x": x,
                    "y": y,
                    "z": z,
                    "total_fuel": total_fuel,
                    "mean_fuel_second": total_fuel/step,
                    "fuel_last_step": instant_fuel_consuption2,
                    "speed_recommended": r*max_speed_caminhao,
                    "step": step,
                    "speed": speed,
                    "mean_speed": mean_speed/step
                    })
            except Exception as e:
                print("######################")
                print(e)
                print("######################")
                continue
                # raise e
                pass





    except Exception as e:
        # print("######################")
        # print(e)
        # print("######################")
        raise e


    for i in range(len(pdf)):
        pdf[i] = float(pdf[i]*100)/float(npdf)
    
    pdffile = ""

    if type(model)!=str and model!="fuzzy":
        pdffile = 'PDF/results/sumo(MODEL){}.csv'.format(sim_atual)
    elif model=="fuzzy":
        pdffile = 'PDF/results/sumo(FUZZY){}.csv'.format(sim_atual)
    elif model=="fuzzy2":
        pdffile = 'PDF/results/sumo(FUZZY2){}.csv'.format(sim_atual)
    else:
        pdffile = 'PDF/results/sumo(default_sumo){}.csv'.format(sim_atual)
 
    if os.path.exists(pdffile):
        os.remove(pdffile)
    resultFile = open(pdffile, 'a')
    sim_atual += 1
    for i in range(len(pdf)):
        mean_speed +=  i*pdf[i]
        # print('i: ', i, ' pdf: ', pdf[i], ' i*pdf: ', i*pdf[i])
        resultFile.write("{}{}{}{}".format(i,':',pdf[i],'\n'))

    resultFile.close()

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


    fig, ax = plt.subplots(3,1,figsize=(20,5))
    for i in range(len(extras)):
        # if i>10: break

        inf = extras[i]
        xs.append(inf["x"])
        ys.append(inf["z"]+z_add)
        ys_green_above.append(inf["z"]+z_add+5)
        ys_green_below.append(inf["z"]+z_add-5)


        # if i%50==0 and i%100!=0:
        #     ax[0].annotate(str(round(inf["angle"],1)),
        #                 xy=(inf["x"], inf["z"]+z_add+5), xycoords='data',
        #                 xytext=(5, 40), textcoords='offset points',
        #                 arrowprops=dict(arrowstyle="->"),
        #                 horizontalalignment='right', verticalalignment='bottom')

    # ax[0].set_ylim(0,300)

    index = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30])
    y_label  = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30']
    
    ax[2].set_yticks(index)
    ax[2].set_yticklabels(y_label)

    ax[1].grid(True, which="both", ls="-", linewidth=0.1, color='0.10', zorder=0)   
    ax[2].grid(True, which="both", ls="-", linewidth=0.1, color='0.10', zorder=0)   
    ax[0].patch.set_facecolor('#87d3e0')
    ax[0].set_xlim(-20,xs[-1]+20)
    ax[1].set_xlim(-20,xs[-1]+20)
    ax[2].set_xlim(-20,xs[-1]+20)
    ax[2].set_ylim(22,30)
    # ax[3].set_xlim(-20,xs[-1]+20)
    ax[0].stackplot(xs, ys_green_above, color="#269126")
    ax[0].stackplot(xs, ys, color="#000000")
    ax[0].stackplot(xs, ys_green_below, color="#269126")
    ax[0].set_title('Elevation for Map '+nome.replace(".net.xml",""))
    ax[0].set_xlabel('Distance [m]')
    ax[0].set_ylabel('Height [m]')




    entradas = [
        "Model",
        "Fuzzy",
        "Fuzzy2",
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



    ax[1].set_xlabel('Distance [m]')
    ax[1].set_ylabel('Instant Fuel [l/s]')

    # ax[1].legend()


    for e in entradas:
        xs = []
        ys = []
        total = 0
        for a in dados[e]:
            xs.append(a['x'])
            ys.append(a['speed'])
            total = a['total_fuel']
        if len(xs)>0:
            if e == 'Model':
               e = 'Neural Network' 
            if e == 'Krauss':
               e = 'SUMO' 
            # ax[2].plot(xs, ys, label="{} ({})".format(e,total))
            ax[2].plot(xs, ys, label=e)



    if len(dados["Model"])>0:
        xs = []
        ys = []
        for a in dados["Model"]:
            xs.append(a['x'])
            ys.append(a['speed_recommended'])
        if len(xs)>0:
            ax[2].plot(xs, ys, dashes=[6, 2], label="Recommended", color="#bd1111")
            # ax[3].plot([], [], dashes=[6, 2], label="Model Recommended", color="#bd1111")


    ax[2].set_xlabel('Distance [m]')
    ax[2].set_ylabel('Speed [m/s]')
    # ax[2].legend()

    # for e in entradas:
    #     xs = []
    #     ys = []
    #     total = 0
    #     for a in dados[e]:
    #         xs.append(a['x'])
    #         ys.append(a['total_fuel'])
    #         total = a['total_fuel']

    #     total = round(total,1)
    #     if len(xs)>0:
    #         if e=="Krauss":
    #             e = "SUMO"
    #         ax[3].plot(xs, ys, label="{} ({})".format(e,total))


    


    # ax[3].set_xlabel('Distance (m)')
    # ax[3].set_ylabel('Total Fuel')
    ax[2].legend()
    ax[2].legend(loc='lower center', bbox_to_anchor=(0.83, 3.4),
              ncol=3, fancybox=True, shadow=True)

    plt.savefig("./mapas/FINAL_"+nome+".png", bbox_inches="tight")
    plt.close()
    # break



def main(arquivo):
    f = open(arquivo,"r")
    dado = json.loads(f.read())
    f.close()
    gen = dado["historic"][0]["best_genome"]
    gen = converter(gen)
    model = get_model()
    model.set_weights(gen)



    folder = "./mapas/"
    mapas = os.listdir(folder)

    mapas = [mapa for mapa in mapas if mapa.split(".")[-1]=="xml" and mapa.split(".")[-2]=="net"]
    # mapas = ['15.net.xml']
    # return
    resultados_obtidos = {}
    for m in mapas:
        resultados_obtidos[m] = {"Model":[],"Krauss":[],"KraussOrig1":[],"KraussPS":[],"PWagner2009":[],"IDM":[],"Wiedemann":[],"W99":[],"Fuzzy":[],"Fuzzy2":[]}
        print("_______Model______________")
        resultados_obtidos[m]["Model"] = start_simulation("sumo", (folder+m).replace(".net.xml",".sumo.cfg"), (folder+m), model, m)
        print("_______Krauss______________")
        resultados_obtidos[m]["Krauss"]   = start_simulation("sumo", (folder+m).replace(".net.xml",".sumo.cfg"), (folder+m), "Krauss", m)
        # # print("_______KraussOrig1______________")
        # # resultados_obtidos[m]["KraussOrig1"]   = start_simulation("sumo", (folder+m).replace(".net.xml",".sumo.cfg"), (folder+m), "KraussOrig1", m)
        # print("_______KraussPS______________")
        # resultados_obtidos[m]["KraussPS"]   = start_simulation("sumo", (folder+m).replace(".net.xml",".sumo.cfg"), (folder+m), "KraussPS", m)
        # # print("_______PWagner2009______________")
        # # resultados_obtidos[m]["PWagner2009"]   = start_simulation("sumo", (folder+m).replace(".net.xml",".sumo.cfg"), (folder+m), "PWagner2009", m)
        # # print("_______IDM______________")
        # # resultados_obtidos[m]["IDM"]   = start_simulation("sumo", (folder+m).replace(".net.xml",".sumo.cfg"), (folder+m), "IDM", m)
        # # print("_______Wiedemann______________")
        # # resultados_obtidos[m]["Wiedemann"]   = start_simulation("sumo", (folder+m).replace(".net.xml",".sumo.cfg"), (folder+m), "Wiedemann", m)
        # # print("_______W99______________")
        # # resultados_obtidos[m]["W99"]   = start_simulation("sumo", (folder+m).replace(".net.xml",".sumo.cfg"), (folder+m), "W99", m)
        print("_______Fuzzy______________")
        resultados_obtidos[m]["Fuzzy"] = start_simulation("sumo", (folder+m).replace(".net.xml",".sumo.cfg"), (folder+m), "fuzzy", m)
        print("_______Fuzzy2______________")
        resultados_obtidos[m]["Fuzzy2"] = start_simulation("sumo", (folder+m).replace(".net.xml",".sumo.cfg"), (folder+m), "fuzzy2", m)


        # print(resultados_obtidos[m]["Model"])

    #     file = open(folder+m.replace(".net.xml",".extras"),"r")
    #     extras = json.loads(file.read())
    #     file.close()


    #     plow(resultados_obtidos[m], extras, m)
    #     # break

    # f = open("final_res_complete.json","w")
    # f.write(json.dumps(resultados_obtidos))
    # f.close()

if __name__ == '__main__':
    
    # a = "./results/20_20_True_0.1.json"
    a = "./results/20_200_True_0.1.json"
    main(a)
