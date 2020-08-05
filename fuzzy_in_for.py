# Fuzzy Logic in Pyhton - Speed Control

# The problem is to define the speed value in a card based on road features.

# Input (antecedents):

# INPUT 0: Instantaneous Speed (IS) (range of crisp values): 0 to 30 Fuzzy set (fuzzy values): low, medium, high
# INPUT 1: Road gradient (RG) (range of crisp values): -1 to 1 Fuzzy set (fuzzy values): low, medium, high
# INPUT 2: Elevetion 10m ahead (A10) (range of crisp values): -1 to 1 Fuzzy set (fuzzy values): low, medium, high
# INPUT 3: Elevetion 50m ahead (E50) (range of crisp values): -1 to 1 Fuzzy set (fuzzy values): low, medium, high

# Output (consequent):
# OUTPUT 1: Speed Universe (S) (crisp values): 0 to 1 Fuzzy set (fuzzy values): verylow, low, medium, high, veryhigh

# Rules
# IF RG is negative THEN S is high
# IF RG is neutral and A10 is low THEN S is high
# IF RG is neutral and A10 is high THEN S is medium
# IF RG is postive and A10 is low THEN S is high
# IF RG is postive and A10 is high THEN S is medium
# IF RG is postive and IS is low THEN S is low

import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class Algorithm:
    
    S_simulator = None

    def __init__(self):

        maxSpeed = 30
        mimSpeed = 22 
        maxAngle = 45
        mimAngle = -45
        maxIS = 30
        mimIS = 0

        # Create the problem variables
        IS = ctrl.Antecedent(np.arange(mimIS, maxIS + 1, 1), 'IS')
        RG = ctrl.Antecedent(np.arange(mimAngle, maxAngle + 1, 1), 'RG')
        A10 = ctrl.Antecedent(np.arange(mimAngle, maxAngle, 1), 'A10')
        A30 = ctrl.Antecedent(np.arange(mimAngle, maxAngle, 1), 'A30')
        A50 = ctrl.Antecedent(np.arange(mimAngle, maxAngle, 1), 'A50')
        A70 = ctrl.Antecedent(np.arange(mimAngle, maxAngle, 1), 'A70')

        S = ctrl.Consequent(np.arange(mimSpeed, maxIS + 1, 1), 'S')

        # Automatically creates mapping between crisp and fuzzy values
        # using a standard membership function (triangle)
        IS.automf(names=['low', 'medium', 'high'])
        S.automf(names=['verylow','low', 'medium', 'high','veryhigh'])

        A10['negative'] = fuzz.gaussmf(A10.universe, mimAngle, 30)
        A10['neutral'] = fuzz.gaussmf(A10.universe, 0, 30)
        A10['positive'] = fuzz.gaussmf(A10.universe, maxAngle, 30)

        A30['negative'] = fuzz.gaussmf(A10.universe, mimAngle, 30)
        A30['neutral'] = fuzz.gaussmf(A10.universe, 0, 30)
        A30['positive'] = fuzz.gaussmf(A10.universe, maxAngle, 30)

        A50['negative'] = fuzz.gaussmf(A10.universe, mimAngle, 30)
        A50['neutral'] = fuzz.gaussmf(A10.universe, 0, 30)
        A50['positive'] = fuzz.gaussmf(A10.universe, maxAngle, 30)       

        # Creates membership functions using different types
        RG['negative'] = fuzz.gaussmf(RG.universe, mimAngle, 40) # 50
        RG['neutral'] = fuzz.gaussmf(RG.universe, 0, 30)
        RG['positive'] = fuzz.gaussmf(RG.universe, maxAngle,50)
   
        
        rule1 = ctrl.Rule(RG['negative'] & A10['negative'], S['veryhigh'])        
        rule2 = ctrl.Rule(RG['negative'] & A10['positive'], S['verylow'])
        rule3 = ctrl.Rule(RG['negative'] & A30['neutral'], S['veryhigh']) 
        rule4 = ctrl.Rule(RG['negative'] & A10['neutral'] & A30['positive'], S['high'])
        rule5 = ctrl.Rule(RG['positive'] & A30['positive'], S['medium'])        
        rule6 = ctrl.Rule(RG['positive'] & A10['neutral'], S['low'])
        rule7 = ctrl.Rule(RG['positive'] & A30['negative'], S['high'])
        rule8 = ctrl.Rule(RG['neutral'] & A10['neutral'], S['high'])        
        rule9 = ctrl.Rule(RG['neutral'] & A10['positive'], S['high'])
        rule10 = ctrl.Rule(RG['neutral'] & A10['positive'] & A50['neutral'], S['high'])
        rule11 = ctrl.Rule(RG['neutral'] & A10['positive'] & A50['negative'], S['medium']) #IS

        # Creating and simulating a fuzzy controller
        S_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11])
        self.S_simulator = ctrl.ControlSystemSimulation(S_ctrl)
   
    def findSpeed(self, speed, angle, inf10, inf30, inf50, inf70):

        self.S_simulator.input['RG'] = angle  # Road gradient (-90, 90) grados
        self.S_simulator.input['A10'] = inf10 # Road gradient (-90, 90) grados
        self.S_simulator.input['A30'] = inf30 # Road gradient (-90, 90) grados
        self.S_simulator.input['A50'] = inf50 # Road gradient (-90, 90) grados

        # Computing the result
        self.S_simulator.compute()
        # print('Speed:', self.S_simulator.output['S'], 'm/s')
        
        return(self.S_simulator.output['S'])
        plt.show()
