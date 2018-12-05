import pandas as pd
import datetime
import matplotlib.pyplot as plt

# got the csv from: url = 'https://datatank.stad.gent/4/mobiliteit/fietstellingencoupure.csv?limit=200000'

# load all the data in the records list
print("reading records from file")
records = []

with open('files/fietstellingencoupure.csv', 'r') as f:
    for line in f:
        date_str, time_str, north, south  = line.split(';')
        date = datetime.datetime(int(date_str.split('/')[2]), int(date_str.split('/')[1]), int(date_str.split('/')[0]))
        records.append({
            'date': date,
            'month': int(date_str.split('/')[1]),
            'year': int(date_str.split('/')[2]),
            'hour': int(time_str.split(':')[0]),
            'weekday': True if date.weekday() < 5 else False,
            'north': int(north),
            'south': int(south),
            'total': int(north) + int(south)
            })

# load data in pandas dataframe
df = pd.DataFrame(records)

week_days = df.loc[df['weekday'] == True]
weekend_days = df.loc[df['weekday'] == False]

# hour graphs
hourly = df.groupby(['hour']).mean()

plt.figure()
plt.plot(hourly.index, hourly['total'])
plt.axis([0, 24, 0, 500])
for a,b in zip(hourly.index, hourly['total']): 
    plt.text(a-1, b+10, str(int(b)))
plt.savefig('plots/hourly_bikes')

plt.figure()
plt.bar(hourly.index, hourly['total'], align='edge', tick_label=hourly.index)
plt.title('average hourly counts at coupure')
plt.axis([0, 24, 0, 200])
plt.savefig('plots/hourly_bikes_barchart')

week_day_hourly = week_days.groupby(['hour']).mean()

plt.figure()
plt.bar(week_day_hourly.index, week_day_hourly['total'], align='edge', tick_label=week_day_hourly.index)
plt.title('average hourly counts at coupure on week day')
plt.axis([0, 24, 0, 200])
plt.savefig('plots/hourly_bikes_week_day_barchart')

weekend_day_hourly = weekend_days.groupby(['hour']).mean()

plt.figure()
plt.bar(weekend_day_hourly.index, weekend_day_hourly['total'], align='edge', tick_label=weekend_day_hourly.index)
plt.title('average hourly counts at coupure on weekend days')
plt.axis([0, 24, 0, 200])
plt.savefig('plots/hourly_bikes_weekend_day_barchart')

# Gent festival effect?
gf16_start = datetime.datetime(2016, 7, 15)
gf16_end =  datetime.datetime(2016, 7, 24)
gf16 = df.query('date >= @gf16_start and date <= @gf16_end')

gf16_hourly = gf16.groupby(['hour']).mean()

plt.figure()
plt.bar(gf16_hourly.index, gf16_hourly['total'], align='edge', tick_label=gf16_hourly.index)
plt.title('average hourly counts at coupure during Gent festival 2016')
plt.axis([0, 24, 0, 200])
plt.savefig('plots/hourly_bikes_gf16_barchart')

gf15_start = datetime.datetime(2015, 7, 13)
gf15_end =  datetime.datetime(2015, 7, 22)
gf15 = df.query('date >= @gf15_start and date <= @gf15_end')

gf15_hourly = gf15.groupby(['hour']).mean()

plt.figure()
plt.bar(gf15_hourly.index, gf15_hourly['total'], align='edge', tick_label=gf15_hourly.index)
plt.title('average hourly counts at coupure during Gent festival 2015')
plt.axis([0, 24, 0, 200])
plt.savefig('plots/hourly_bikes_gf15_barchart')

gf14_start = datetime.datetime(2014, 7, 13)
gf14_end =  datetime.datetime(2014, 7, 22)
gf14 = df.query('date >= @gf14_start and date <= @gf14_end')

gf14_hourly = gf14.groupby(['hour']).mean()

plt.figure()
plt.bar(gf15_hourly.index, gf14_hourly['total'], align='edge', tick_label=gf14_hourly.index)
plt.title('average hourly counts at coupure during Gent festival 2014')
plt.axis([0, 24, 0, 200])
plt.savefig('plots/hourly_bikes_gf14_barchart')