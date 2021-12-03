# Title: Solar-Storage hybrid Model
# Author of code: Ankitkumar B Maddewad
# Title: 3rd Dec 2021

# Design an economic dispatch model to serve a load. Load data for a week is given in accompanying excel file.
# Assume 3 generators
# 1. Diesel Plant 20 MW – 2000 rs/MWh
# 2. Coal plant 40 MW – 3000 rs/MWh
# 3. Natural Gas Plant 30 MW- 10000 rs/MWh
# Assume infinite ramps rates for coal and gas plants
# Express outputs in area charts and write data to excel

import pandas as pd
from matplotlib import pyplot as plt
import pulp as p
load = pd.read_excel('load.xlsx')
load_df = pd.DataFrame(load)
# load_df.set_index(load_df['Time Stamp'],inplace = False)
load_df = load_df.loc[:,['Time Stamp','Load (MW)']]

# case 1 :
# cost fun = 2000*p1 + 3000*p2 + 10000*p3
# p1 + p2 + p3 = x
# 0 <= p1 <= 20
# 0 <= p2 <= 40
# 0 <= p3 <= 30
  
P1 = []
P2 = []
P3 = []
C = []
for x in load_df['Load (MW)']:
# Create a LP Minimization problem

    Lp_prob = p.LpProblem('Problem', p.LpMinimize) 
    
    # Create problem Variables 
    p1 = p.LpVariable("p1", lowBound = 0)   # Create a variable p1 >= 0
    p2 = p.LpVariable("p2", lowBound = 0)   # Create a variable p2 >= 0
    p3 = p.LpVariable("p3", lowBound = 0)   # Create a variable p3 >= 0
    c = p.LpVariable("c", lowBound = 0)   # Create a variable p3 >= 0
    # Objective Function
    # Lp_prob += 3 * x + 5 * y   

    # Objective Function
    Lp_prob += 2000*p1 + 3000*p2 + 10000*p3
    
    # Constraints:
    # Lp_prob += 2 * x + 3 * y >= 12
    # Lp_prob += -x + y <= 3
    # Lp_prob += x >= 4
    # Lp_prob += y <= 3

    Lp_prob += p1 + p2 + p3 - c >= x
    Lp_prob += p1 <= 20
    Lp_prob += p2 <= 40
    Lp_prob += p3 <= 30
    # Lp_prob += c <= 0.1

    status = Lp_prob.solve()
    # print(p.LpStatus[status])   # The solution status

    # Printing the final solution
    # print(p.value(p1), p.value(p2),p.value(p3),p.value(c), p.value(Lp_prob.objective))
    P1.append(p.value(p1))
    P2.append(p.value(p2))
    P3.append(p.value(p3))
    # C.append(p.value(c))

load_df['P1'] = P1
load_df['P2'] = P2
load_df['P3'] = P3
# load_df['C'] = C
# print(load_df)
# print(P3)

load_df.to_csv('Economic load dispatch with LPP.csv')
# data = pd.read_csv('Economic load dispatch with LPP.csv')
# load_df = pd.DataFrame(data)

plt.style.use('seaborn')
plt.stackplot(load_df['Time Stamp'].tolist(), load_df['P1'].tolist(),load_df['P2'].tolist(),load_df['P3'].tolist())
plt.legend(['Diesel plant','Coal plant','Natural gas plant'])
plt.stackplot(load_df['Time Stamp'].tolist(), load_df['P1'].tolist(),load_df['P2'].tolist(),load_df['P3'].tolist())
plt.title('Economic Load Dispatch')
plt.xlabel('Time Stamp')
plt.ylabel('Load shared')
plt.show()