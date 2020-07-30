# Fuzzy Logic in Pyhton - Speed Control

# The problem is to define the speed value in a card based on road features.

# Input (antecedents):

# INPUT 0: Instantaneous Speed (IS) (range of crisp values): 0 to 30 Fuzzy set (fuzzy values): low, medium, high
# INPUT 1: Road gradient (RG) (range of crisp values): -1 to 1 Fuzzy set (fuzzy values): negative, neutral, positive
# INPUT 2: Elevetion 10m ahead (E10) (range of crisp values): -1 to 1 Fuzzy set (fuzzy values): low, medium, high
# INPUT 3: Elevetion 50m ahead (E50) (range of crisp values): -1 to 1 Fuzzy set (fuzzy values): low, medium, high

# Output (consequent):
# OUTPUT 1: Speed Universe (S) (crisp values): 0 to 1 Fuzzy set (fuzzy values): verylow, low, medium, high, veryhigh

# Rules
# IF RG is negative THEN S is high
# IF RG is neutral and E10 is low THEN S is high
# IF RG is neutral and E10 is high THEN S is medium
# IF RG is postive and E10 is low THEN S is high
# IF RG is postive and E10 is high THEN S is medium
# IF RG is postive and IS is low THEN S is low


import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Create the problem variables
IS = ctrl.Antecedent(np.arange(0, 31, 1), 'IS')
RG = ctrl.Antecedent(np.arange(-90, 91, 1), 'RG')
E10 = ctrl.Antecedent(np.arange(-25, 26, 1), 'E10')


S = ctrl.Consequent(np.arange(0, 31, 1), 'S')

# Automatically creates mapping between crisp and fuzzy values
# using a standard membership function (triangle)
IS.automf(names=['low', 'medium', 'high'])

# Creates membership functions using different types
RG['negative'] = fuzz.gaussmf(RG.universe, -90, 50)
RG['neutal'] = fuzz.gaussmf(RG.universe, 0, 30)
RG['positive'] = fuzz.gaussmf(RG.universe, 90,50)

E10.automf(names=['low', 'medium', 'high'])

S['verylow'] = fuzz.trimf(S.universe, [0, 0, 9])
S['low'] = fuzz.trapmf(S.universe, [3, 6, 10, 15])
S['medium'] = fuzz.trimf(S.universe, [9, 15, 21])
S['high'] = fuzz.trapmf(S.universe, [15, 20, 24, 27])
S['veryhigh'] = fuzz.trimf(S.universe, [21, 30, 30])

# Graphically showing the created parting functions

# IS.view()
# RG.view()
# E10.view()
# S.view()

# Fuzzy rules creation

# IF RG is negative THEN S is high
rule1 = ctrl.Rule(RG['negative'], S['veryhigh'])

# IF RG is neutral and E10 is low THEN S is high
rule2 = ctrl.Rule(RG['neutal'] & E10['low'], S['high'])

# IF RG is neutral and E10 is high THEN S is medium
rule3 = ctrl.Rule(RG['neutal'] & E10['high'], S['medium'])

# IF RG is postive and E10 is low THEN S is high
rule4 = ctrl.Rule(RG['positive'] & E10['low'], S['high'])

# IF RG is postive and E10 is high THEN S is medium
rule5 = ctrl.Rule(RG['positive'] & E10['high'], S['medium'])

# IF RG is postive and IS is low THEN S is low
rule6 = ctrl.Rule(RG['positive'] & IS['low'], S['low'])


# Creating and simulating a fuzzy controller

S_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
S_simulator = ctrl.ControlSystemSimulation(S_ctrl)

# Entering some values for quality of IS and RG
S_simulator.input['IS'] = 3 # Instantaneous Speed (0, 30) m/s
S_simulator.input['RG'] = -50  # Road gradient (-90, 90) grados
S_simulator.input['E10'] = -5 # Elevetion 10m ahead (-25, 25) metros

# Computing the result
S_simulator.compute()
print('Speed:', S_simulator.output['S'], 'm/s')

# Graphically showing the result
# IS.view(sim=S_simulator)
# RG.view(sim=S_simulator)
# S.view(sim=S_simulator) 

plt.show()
