# Title: SOlar-Storage hybrid Model
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
load = pd.read_excel('load.xlsx')
load_df = pd.DataFrame(load)
# load_df.set_index(load_df['Time Stamp'],inplace = False)
load_df = load_df.loc[:,['Time Stamp','Load (MW)']]

# print(load_df.head())
P1 = []
P2 = []
P3 = []
# The given incremental costs are constant so variation in load have no effect on the Incremental cost.
# Therfore they can be directly used at their maximum capacity

for idx,x in enumerate(load_df['Load (MW)']):
    # case 1 :
    # cost fun = 2000*p1 + 3000*p2 + 10000*p3
    # p1 + p2 + p3 = x
    # 0 <= p1 <= 20
    # 0 <= p2 <= 40
    # 0 <= p3 <= 30

    # case 2:
    # considering constant incremental cost & infinite ramp rates, Generating unit with less incremental cost will share more load and contrast.
    if x >= 20:
        p1 = 20
        if (x-p1) >= 40:
            p2 = 40
            if (x-p1-p2) >= 30:
                p3 = 30
            else:
                p3 = (x - p1 - p2)
        else:
            p2 = (x-p1)
            p3 = 0
    else:
        p1 = x
        p2 = 0
        p3 = 0
    P1.append(p1)
    P2.append(p2)
    P3.append(p3)
load_df['P1'] = P1
load_df['P2'] = P2
load_df['P3'] = P3

print(load_df)

load_df.to_csv('Economic load dispatch.csv')
# data = pd.read_csv('Economic load dispatch.csv')
# load_df = pd.DataFrame(data)

plt.style.use('seaborn')
plt.stackplot(load_df['Time Stamp'].tolist(), load_df['P1'].tolist(),load_df['P2'].tolist(),load_df['P3'].tolist())
plt.legend(['Diesel plant','Coal plant','Natural gas plant'])
plt.stackplot(load_df['Time Stamp'].tolist(), load_df['P1'].tolist(),load_df['P2'].tolist(),load_df['P3'].tolist())
plt.title('Economic Load Dispatch')
plt.xlabel('Time Stamp')
plt.ylabel('Load shared')
plt.show()


