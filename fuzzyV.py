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


        maxIS = 30
        mimIS = 0 

        maxAngle = 70
        mimAngle = -70

        # Create the problem variables
        IS = ctrl.Antecedent(np.arange(mimIS, maxIS + 1, 1), 'IS')
        RG = ctrl.Antecedent(np.arange(mimAngle, maxAngle + 1, 1), 'RG')
        A10 = ctrl.Antecedent(np.arange(mimAngle, maxAngle, 1), 'A10')
        A30 = ctrl.Antecedent(np.arange(mimAngle, maxAngle, 1), 'A30')
        A50 = ctrl.Antecedent(np.arange(mimAngle, maxAngle, 1), 'A50')
        A70 = ctrl.Antecedent(np.arange(mimAngle, maxAngle, 1), 'A70')


        S = ctrl.Consequent(np.arange(0, 31, 1), 'S')

        # Automatically creates mapping between crisp and fuzzy values
        # using a standard membership function (triangle)
        IS.automf(names=['low', 'medium', 'high'])

        A10.automf(names=['negative', 'neutral', 'positive'])
        A30.automf(names=['negative', 'neutral', 'positive'])
        A50.automf(names=['negative', 'neutral', 'positive'])
        A70.automf(names=['negative', 'neutral', 'positive'])

        # Creates membership functions using different types
        RG['negative'] = fuzz.gaussmf(RG.universe, -90, 50)
        RG['neutral'] = fuzz.gaussmf(RG.universe, 0, 30)
        RG['positive'] = fuzz.gaussmf(RG.universe, 90,50)


        S['verylow'] = fuzz.trimf(S.universe, [0, 0, 9])
        S['low'] = fuzz.trapmf(S.universe, [3, 6, 10, 15])
        S['medium'] = fuzz.trimf(S.universe, [9, 15, 21])
        S['high'] = fuzz.trapmf(S.universe, [15, 20, 24, 27])
        S['veryhigh'] = fuzz.trimf(S.universe, [21, 30, 30])

        # Graphically showing the created parting functions
        # IS.view()
        # RG.view()
        # A10.view()
        # A30.view()
        # A50.view()
        # A70.view()
        # S.view()
   
        #rule1 = ctrl.Rule(RG['negative'], S['veryhigh'])
        rule1 = ctrl.Rule(RG['negative'] & A10['negative'], S['veryhigh'])
 
        #rule2 = ctrl.Rule(RG['neutral'] & A10['negative'], S['high'])
        rule2 = ctrl.Rule(RG['negative'] & A30['positive'], S['verylow'])

        #rule3 = ctrl.Rule(RG['neutral'] & A10['negative'] & A30['positive'], S['veryhigh'])
        rule3 = ctrl.Rule(RG['positive'] & A30['positive'], S['medium'])

        #rule4 = ctrl.Rule(RG['neutral'] & A10['negative'], S['high'])
        rule4 = ctrl.Rule(RG['positive'] & A10['neutral'], S['high'])

        #rule5 = ctrl.Rule(RG['positive'] & A30['negative'], S['high'])
        rule5 = ctrl.Rule(RG['positive'] & A30['negative'], S['veryhigh'])

        #rule6 = ctrl.Rule((RG['positive'] & IS['low']), S['medium'])
        rule6 = ctrl.Rule(RG['neutral'] & A10['neutral'], S['veryhigh'])

        rule7 = ctrl.Rule(RG['neutral'] & A10['positive'], S['medium'])
        
         
        # Creating and simulating a fuzzy controller
        S_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7])
        self.S_simulator = ctrl.ControlSystemSimulation(S_ctrl)

        # Entering some values for quality of IS and RG
    
   
    def findSpeed(self, speed, angle, inf10, inf30, inf50, inf70):

        # print("Running Fuzzy")
        
        self.S_simulator.input['IS'] = speed # Instantaneous Speed (0, 30) m/s
        self.S_simulator.input['RG'] = angle  # Road gradient (-90, 90) grados
        self.S_simulator.input['A10'] = inf10 # Road gradient (-90, 90) grados
        self.S_simulator.input['A30'] = inf30 # Road gradient (-90, 90) grados
        #self.S_simulator.input['A50'] = inf50 # Road gradient (-90, 90) grados
        # self.S_simulator.input['A70'] = inf70 # Road gradient (-90, 90) grados

        # Computing the result
        self.S_simulator.compute()
        # print('Speed:', self.S_simulator.output['S'], 'm/s')

        # Graphically showing the result
        # IS.view(sim=S_simulator)
        # RG.view(sim=S_simulator)
        # S.view(sim=S_simulator) 
        
        return(self.S_simulator.output['S'])
        plt.show()
