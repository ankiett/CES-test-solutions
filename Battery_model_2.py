# Title: Storage Battery Model
# Author of code: Ankitkumar B Maddewad
# Title: 2nd Dec 2021

# Problem statement 1: Implement a Storage Battery model of 1 MW / 2MWh which charges in morning (assume any suitable time) and discharges in evening (assume any suitable time) every day for a year. Assume data frequency of simulation to be of 15 min. Consider parameters like charging efficiency (~92%), discharge efficiency (~92%). Assume data wherever necessary.
# Express data in suitable charts (plotly preferred). Also the model should write the data in excel/csv to review data manually
# Output data expected (35040 points each):
# • SoC – MWh/%
# • Charging units – MW
# • Discharging units – MW
# • Time stamp

# Given & assumed data
    # Rated power capacity = 1 MW
    # Energy capacity = 2 MWh
    # Charges in 10 am to 4 pm
    # Discharges in 7 pm to 11 pm
    # Charging efficiecy = 92%
    # Discharging efficiency = 92%
    #  Charging and Discharging rates are assumed to be uniform
    # c rate of battery is generally measured in c 
    # For convenience, it will be measured in MWh/hr representing energy units stored/discharged per hour
    # Chargin rate(case 1) = 0.3 MWh/hr i.e. # C rate per time division = 0.075MW/15 min div
    # Charging rate(case 2) = 1.8 kAh
    # Discharge rate(case 1) = 0.6 MWh/hr i.e. # D rate per time division = 0.15 MW/15 min div
    # Discharge rate(case 2) = 1.8 kAh

# case 1
import datetime as dt
import pandas as pd
from matplotlib import pyplot as plt

Energy_cap = 2 # 2MWh
timestamp = dt.datetime.now()
C_Units = 0
D_Units = 0
SoC = 0
SOC = C_Units + D_Units
instance = [[timestamp,SoC,SOC,C_Units,D_Units]]
df = pd.DataFrame(instance, columns = ['Time stamp', 'SoC (in %)','SoC (in MWh)','Charging Units (in MW)','Discharging Units (in MW)'])

now = dt.datetime.now()

while len(df)<=35039:
# while False:
    if now.hour >= 11 and now.hour < 16:
        # print('Battery Status: Charging')
        timestamp = now + dt.timedelta(0, 900)
        # print(timestamp)
        C_Units = 0.075 * 0.92
        D_Units =  0
        SOC += (C_Units + D_Units)
        SoC = (SOC/Energy_cap)*100
        instance = [timestamp, SoC,SOC, C_Units, D_Units]
        df.loc[len(df)] = instance
        # print(instance)
    else:
        if now.hour>= 19 and now.hour < 23 and SOC > 0:
            # print('Battery Status: Discharging')
            timestamp = now + dt.timedelta(0, 900)
            # print(timestamp, type(timestamp))
            C_Units = 0
            D_Units = -0.15*1.086
            if abs(D_Units) > SOC:
                SOC = 0 
                D_Units = SOC
            else:
                SOC += (C_Units + D_Units)
            SoC = (SOC/Energy_cap)*100
            instance = [timestamp, SoC,SOC, C_Units, D_Units]
            df.loc[len(df)] = instance
            # print(instance)
        else:
            # now.hour>= 23 and now.hour < 11:
            # print('Battery Status: Idle')
            timestamp = now + dt.timedelta(0, 900)
            # print(timestamp, type(timestamp))
            C_Units = 0
            D_Units = 0
            SOC += (C_Units + D_Units)*0.92
            SoC = (SOC/Energy_cap)*100
            instance = [timestamp, SoC,SOC, C_Units, D_Units]
            df.loc[len(df)] = instance
            # print(instance)

    now = now + dt.timedelta(0, 900)

# print(df)
df.to_csv('Storage Battery Model data.csv')    # write name of csv file here
plt.style.use('seaborn')
plt.plot_date(df['Time stamp'], df['SoC (in MWh)'], ls = 'solid')
plt.title('Battery SoC chart')
plt.xlabel('Date')
plt.ylabel('SoC in MWh') 
plt.tight_layout()
plt.show()