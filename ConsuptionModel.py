import math
import numpy as np

class ModelConsuption:
    """

    https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwinp4Wsu4DrAhVbILkGHQV4CdsQFjAAegQIBBAB&url=https%3A%2F%2Ffenix.tecnico.ulisboa.pt%2FdownloadFile%2F1970719973965948%2FDissertacao%2520de%2520Mestrado%2520Final%2520-%2520Rodrigo%2520Hibon%2520de%2520Campos%2520Dias%2520de%2520Carvalho.pdf&usg=AOvVaw02ZIJFgwG1_nxDR2QLAQnY
    Metodologia de Cálculo de Consumos de Combustível e Emissões de Poluentes Baseada em Perfis de Condução

    """

    def __init__(self, speed, accel, slope):
        self.speed = speed
        self.accel = accel
        self.slope = slope               

    def calc_vsp(self):
        # VSP : Vehicle Specific Power
        # velocidade : m/s
        # aceleracao : m/s^2
        # slope : graus - > radianos
        degree = math.radians(self.slope)
        rollingResist = 0.132 # m/s^2
        aerodynamicResist = 0.000302 # m^-1

        accelGravity = 9.8 # m/s^2

        vsp = (self.speed * (1.1 * self.accel + (accelGravity * math.sin(degree)) + rollingResist)) + (aerodynamicResist * (self.speed ** 3))
        
        return vsp

    def mapping_mode_vsp(self, vsp):

        if vsp < -2:
            mode = 1
        elif vsp < 0:
            mode = 2
        elif vsp < 1:
            mode = 3
        elif vsp < 4:
            mode = 4
        elif vsp < 7:
            mode = 5
        elif vsp < 10:
            mode = 6
        elif vsp < 13:
            mode = 7
        elif vsp < 16:
            mode = 8
        elif vsp < 19:
            mode = 9
        elif vsp < 23:
            mode = 10
        elif vsp < 28:
            mode = 11
        elif vsp < 33:
            mode = 12
        elif vsp < 39:
            mode = 13
        else:
            mode = 14
        
        return mode

    def calc_fuel_consuption(self, mode):

        flag = False
        n = -1000
        media = [0.2, 0.56, 0.69, 1.65, 2.43, 3.11, 3.7, 4.39, 4.81, 5.60, 6.37, 6.88, 7.27, 7.65]
        standardDev = [0.42, 0.72, 0.55, 0.84, 1.01, 1.02, 1.0, 1.02, 0.96, 0.99, 0.88, 0.61, 0.43, 0.01]

        while flag == False:
            n = np.random.normal(0, 0.2, 1)
            if n > -1 and n < 1:
                flag = True

        deviation = n * standardDev[mode-1]
        consuption = media[mode-1] + deviation # galões
        consuption = consuption * 3.78541 # litros
        if consuption[0] < 0:
            consuption[0] = 0
        
        return consuption

    def run(self):
        a = self.calc_vsp()
        b = self.mapping_mode_vsp(a)
        c = self.calc_fuel_consuption(b)
        return c[0]

#speed = 30
#accel = 1
#slope = 5
#modelo = ModelConsuption(speed, accel, slope)
#consuption = modelo.run()
#print(consuption)

