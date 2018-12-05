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
            'dayoftheyear': date.timetuple().tm_yday,
            'month': int(date_str.split('/')[1]),
            'year': int(date_str.split('/')[2]),
            'hour': int(time_str.split(':')[0]),
            'weekday': True if date.weekday() < 5 else False,
            'north': int(north),
            'south': int(south),
            'total': int(north) + int(south)
            })

            
# load data from records in pandas dataframe
df = pd.DataFrame(records)
print(df)

# collect datapoints per day
df = df.groupby(['date','month','year', 'dayoftheyear']).sum().reset_index()

# calculate moving averages to smooth the graphs
df['total avg'] = 0
df['north moving avg'] = 0
df['south moving avg'] = 0
for i, date in enumerate(df['date']):
    try:
        sumnorth = 0
        sumsouth = 0
        for j in range(i-3, i+4):
            sumnorth += df.at[j,'north']
            sumsouth += df.at[j,'south']
        df.at[i,'north moving avg'] = sumnorth / 7
        df.at[i,'south moving avg'] = sumsouth / 7
    except:
        pass
# total avg is the sum of the moving averages for each day in both directions
df['total avg'] = df['north moving avg'] + df['south moving avg']
print(df)

# split the dataframe in 2 week days and weekend days for seperate analysis
week_days = df.loc[df['weekday'] == True]
weekend_days = df.loc[df['weekday'] == False]

# amount of records each day just to control for anomalies
count = df.groupby(['date']).count()

# day graph
daysum2011 = df.query('year == 2011').reset_index()
daysum2012 = df.query('year == 2012').reset_index()
daysum2013 = df.query('year == 2013').reset_index()
daysum2014 = df.query('year == 2014').reset_index()
daysum2015 = df.query('year == 2015').reset_index()
daysum2016 = df.query('year == 2016').reset_index()
daysum2017 = df.query('year == 2017').reset_index()

# vacation periods to show as grey overlay on plot
holidays = [
    {'start': datetime.datetime(2011, 7, 1), 'end': datetime.datetime(2011, 8, 31)},
    {'start': datetime.datetime(2011, 10, 29), 'end': datetime.datetime(2011, 11, 6)},
    {'start': datetime.datetime(2011, 12, 24), 'end': datetime.datetime(2012, 1, 8)},
    
    {'start': datetime.datetime(2012, 2, 18), 'end': datetime.datetime(2012, 2, 26)},
    {'start': datetime.datetime(2012, 3, 31), 'end': datetime.datetime(2012, 4, 15)},
    {'start': datetime.datetime(2012, 7, 1), 'end': datetime.datetime(2012, 8, 31)},
    {'start': datetime.datetime(2012, 10, 27), 'end': datetime.datetime(2012, 11, 4)},
    {'start': datetime.datetime(2012, 12, 22), 'end': datetime.datetime(2013, 1, 6)},

    {'start': datetime.datetime(2013, 2, 9), 'end': datetime.datetime(2013, 2, 17)},
    {'start': datetime.datetime(2013, 3, 30), 'end': datetime.datetime(2013, 4, 14)},
    {'start': datetime.datetime(2013, 7, 1), 'end': datetime.datetime(2013, 8, 31)},
    {'start': datetime.datetime(2013, 10, 25), 'end': datetime.datetime(2013, 11, 2)},
    {'start': datetime.datetime(2013, 12, 21), 'end': datetime.datetime(2014, 1, 5)},
    
    {'start': datetime.datetime(2014, 3, 1), 'end': datetime.datetime(2014, 3, 9)},
    {'start': datetime.datetime(2014, 4, 5), 'end': datetime.datetime(2014, 4, 20)},
    {'start': datetime.datetime(2014, 7, 1), 'end': datetime.datetime(2014, 8, 31)},
    {'start': datetime.datetime(2014, 10, 25), 'end': datetime.datetime(2014, 11, 2)},
    {'start': datetime.datetime(2014, 12, 20), 'end': datetime.datetime(2015, 1, 4)},

    {'start': datetime.datetime(2015, 2, 14), 'end': datetime.datetime(2015, 2, 22)},
    {'start': datetime.datetime(2015, 4, 4), 'end': datetime.datetime(2015, 4, 19)},
    {'start': datetime.datetime(2015, 7, 1), 'end': datetime.datetime(2015, 8, 31)},
    {'start': datetime.datetime(2015, 10, 31), 'end': datetime.datetime(2015, 11, 8)},
    {'start': datetime.datetime(2015, 12, 19), 'end': datetime.datetime(2016, 1, 3)},

    {'start': datetime.datetime(2016, 2, 6), 'end': datetime.datetime(2016, 2, 14)},
    {'start': datetime.datetime(2016, 3, 26), 'end': datetime.datetime(2016, 4, 10)},
    {'start': datetime.datetime(2016, 7, 1), 'end': datetime.datetime(2016, 8, 31)},
    {'start': datetime.datetime(2016, 10, 29), 'end': datetime.datetime(2016, 11, 6)},
    {'start': datetime.datetime(2016, 12, 24), 'end': datetime.datetime(2017, 1, 8)}
]

fig = plt.figure(figsize=(48,6))
plt.plot(daysum2011['date'], daysum2011['total avg'], label='2011')
plt.plot(daysum2012['date'], daysum2012['total avg'], label='2012')
plt.plot(daysum2013['date'], daysum2013['total avg'], label='2013')
plt.plot(daysum2014['date'], daysum2014['total avg'], label='2014')
plt.plot(daysum2015['date'], daysum2015['total avg'], label='2015')
plt.plot(daysum2016['date'], daysum2016['total avg'], label='2016')
plt.plot(daysum2017['date'], daysum2017['total avg'], label='2017')
plt.title('Daily amount of bikes at Coupure (1 week moving average)')
plt.legend(loc='upper left')
plt.ylabel('amount of bikes')
for holiday in holidays:
    plt.axvspan(holiday['start'], holiday['end'], facecolor='0.1', alpha=0.1)
plt.tight_layout()
plt.savefig("plots/daily_bikes.png")


fig = plt.figure(figsize=(12,6))
plt.plot(daysum2011['dayoftheyear'], daysum2011['total avg'], label='2011')
plt.plot(daysum2012['dayoftheyear'], daysum2012['total avg'], label='2012')
plt.plot(daysum2013['dayoftheyear'], daysum2013['total avg'], label='2013')
plt.plot(daysum2014['dayoftheyear'], daysum2014['total avg'], label='2014')
plt.plot(daysum2015['dayoftheyear'], daysum2015['total avg'], label='2015')
plt.plot(daysum2016['dayoftheyear'], daysum2016['total avg'], label='2016')
plt.plot(daysum2017['dayoftheyear'], daysum2017['total avg'], label='2017')
plt.title('Daily amount of bikes at Coupure (1 week moving average)')
plt.legend(loc='upper left')
plt.ylabel('amount of bikes')
plt.xlabel('day of the year')
plt.savefig("plots/daily_bikes_per_year.png")
