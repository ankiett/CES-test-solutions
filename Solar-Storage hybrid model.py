# Title: Solar-Storage hybrid Model
# Author of code: Ankitkumar B Maddewad
# Title: 2nd Dec 2021

# Problem statement 1: Implement Solar/Storage hybrid model. Using the storage model created above, build a solar + storage hybrid model. Assume solar plant to be 5 MW. Assume battery size as above.
# The storage should strictly charge only from solar. Storage should discharge in the eve from 7 pm onwards every day.
# For solar simulation irradiance data can be obtained from pv watts (hourly data; you will need to convert it to 15 min frequency)
# Output data expected (35040 points each):
# • Solar output – MW
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
    # C rate(case 1) = 0.3 MWh/hr i.e. # C rate per time division = 0.075MWhr/15 min div
    # C rate(case 2) = 1.8 kAh
    # D rate(casec 1) = 0.6 MWh/hr i.e. # D rate per time division = 0.15 MWhr/15 min div
    # D rate(case 2) = 1.8kAh

# case 1

import datetime as dt
import pandas as pd
from matplotlib import pyplot as plt

# now = dt.datetime.now()
# print(df)
gen_data = pd.read_csv("Plant_2_Generation_Data.csv") 
# Generation  Data is taken from https://www.kaggle.com/anikannal/solar-power-generation-data?select=Plant_2_Generation_Data.csv
gen_df = pd.DataFrame(gen_data)
daily_gen_data = pd.DataFrame(gen_df['Normalized_gen_data'].dropna())
# print(daily_gen_data,type(daily_gen_data))

# E = A x r x H x PR 
# E is Energy (kWh), A is total Area of the panel (m²), r is solar panel yield (%), 
# H is annual average solar radiation on tilted panels and PR = Performance ratio, constant for losses 
# (range between 0.5 and 0.9, default value = 0.75). r is the yield of the solar panel given by the ratio : 
# electrical power (in kWp) of one solar panel divided by the area of one panel
# 
load_data = pd.read_excel('load.xlsx')
load_df = pd.DataFrame(load_data)
load_df = load_df.iloc[:,[0,3]].dropna()
# print(load_df.head())

Energy_cap = 2 # 2MWh
timestamp = dt.datetime.now()
C_Units = 0
D_Units = 0
SoC = 0
energy_stored = C_Units + D_Units
instance = [[timestamp,SoC,energy_stored,C_Units,D_Units]]
# dti2 = pd.date_range("1/1/2021",periods = 1, freq="15min")
df = pd.DataFrame(instance, columns = ['Time stamp', 'SoC (in %)','SoC (in MWh)','Charging Units (in MW)','Discharging Units (in MW)'])

now = dt.datetime.now()

while len(df)<=350:
# while False:

    if now.hour >= 11 and now.hour < 16 and energy_stored <= 2:
        timestamp = now + dt.timedelta(0, 900)
        instance_no_of_day = now.hour * 4 + now.minute//15 
        excess_gen = daily_gen_data.iloc[instance_no_of_day,0] - load_df.iloc[instance_no_of_day,1]
        if excess_gen > 0 :
            # print('Battery Status: Charging')
            C_Units = excess_gen
            if C_Units >= (2 - energy_stored):
                C_Units = (2 - energy_stored)
                energy_stored = 2
            else:
                energy_stored += C_Units

        SoC = (energy_stored/Energy_cap)*100
        instance = [timestamp, SoC,energy_stored, C_Units, D_Units]
        df.loc[len(df)] = instance
        C_Units = 0
    else:
        if now.hour>= 19 and now.hour < 23 and energy_stored > 0:
            # print('Battery Status: Discharging')
            timestamp = now + dt.timedelta(0, 900)
            C_Units = 0
            D_Units = -0.15*1.086
            if abs(D_Units) > energy_stored:
                energy_stored = 0 
                D_Units = energy_stored
            else:
                energy_stored += (C_Units + D_Units)
            SoC = (energy_stored/Energy_cap)*100
            instance = [timestamp, SoC,energy_stored, C_Units, D_Units]
            df.loc[len(df)] = instance
            D_Units = 0
        else:
            # now.hour>= 23 and now.hour < 11:
            # print('Battery Status: Idle')
            timestamp = now + dt.timedelta(0, 900)
            C_Units = 0
            D_Units = 0
            instance = [timestamp, SoC,energy_stored, C_Units, D_Units]
            df.loc[len(df)] = instance

    now = now + dt.timedelta(0, 900)

print(df.iloc[:,1:].head(80))
# df.to_csv('Solar-Storage hybrid model.csv')    # write name of csv file here
plt.style.use('seaborn')
plt.plot_date(df['Time stamp'], df['SoC (in MWh)'], ls = 'solid')
# plt.plot_date(df['Time stamp'], df['SoC (in %)'], ls = 'solid')
plt.title('Battery Storage SoC chart')
plt.xlabel('Date')
plt.ylabel('SoC in MWh') 
plt.tight_layout()
plt.show()