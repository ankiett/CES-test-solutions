import datetime
import pandas as pd
import numpy as np
from pandas.core.indexes.datetimes import DatetimeIndex
import matplotlib.pyplot as plt
dti = pd.to_datetime(["1/1/2018", np.datetime64("2018-01-01"), datetime.datetime(2018, 1, 1)])   # ??

# print(dti)
dti = pd.date_range("2018-01-03",periods = 3,freq='M')
# print(dti)
# dti = pd.date_range('2020-01-01','2020-12-31',freq = 'D')
ts = pd.Series(range(len(dti)),index=dti)
# print(ts)
ts2 = ts.resample('2H')
# print(ts2)
list = np.random.uniform(5,100,len(dti))
df = pd.DataFrame(index=dti)
df['col'] = np.asarray(list)

# print(df)
# plt.plot(df)
# plt.show()
datestring = "2021 Oct 24th"
# dts = pd.Timestamp(2021,1,13,1,30)
dts = pd.Timestamp(datestring)
deli = pd.Timedelta("1 day")
dts2 = dts - deli - deli;
dts3 = dts + pd.offsets.BDay()
print(dts,dts.day_name(),'\n', dts2,dts2.day_name(),'\n', dts3,dts3.day_name())
# print(dts.day_name())
dts = dts.tz_localize("UTC")
# print(dts)

dts = dts.tz_convert("US/Pacific")
# print(dts)

# print(pd.to_datetime(['2009/07/31', 'asd'], errors='raise'))    # to output the error
# print(pd.to_datetime(['2009/07/31', 'asd'], errors='ignore'))   # return the original input when unparsable
# print(pd.to_datetime(['2009/07/31', 'asd'], errors='coerce'))   # convert unparsable data to NaT(Not a Time)

newseries = pd.Series(range(10),index = pd.date_range('01,10,2021', periods=10, freq ='D'))
# print(newseries)

# How to use periods, periodrange ?? => it's about value in the period of duration unlike instance of datetime stamp

tday = datetime.date.today()
print(tday.isoweekday)
