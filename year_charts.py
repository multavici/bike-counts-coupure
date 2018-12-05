import pandas as pd
import datetime
import matplotlib.pyplot as plt

records = []

# load all the data in the records list
print("reading records from file")
f = open('files/fietstellingencoupure.csv', 'r')
for line in f:
    date_str = line.split(';')[0]
    time_str = line.split(';')[1]
    date = datetime.datetime(int(date_str.split('/')[2]), int(date_str.split('/')[1]), int(date_str.split('/')[0]))
    records.append({
        'date': date,
        'month': datetime.datetime(int(date_str.split('/')[2]), int(date_str.split('/')[1]), 1),
        'year': int(date_str.split('/')[2]),
        'hour': int(time_str.split(':')[0]),
        'weekday': True if date.weekday() < 5 else False,
        'north': int(line.split(';')[2]),
        'south': int(line.split(';')[3]),
        'total': int(line.split(';')[2]) + int(line.split(';')[3])
        })
f.close()

# load data in pandas dataframe
df = pd.DataFrame(records)

week_days = df.loc[df['weekday'] == True]
weekend_days = df.loc[df['weekday'] == False]

# total amount of bikers each year
yearsum = df.groupby(['year']).sum()
yearsum.drop([2011, 2017], inplace=True)

# average daily amount of bikers for each year
yearsum['daily'] = yearsum['total'] // 365

plt.plot(yearsum.index, yearsum['daily'], label='all days')
for a,b in zip(yearsum.index, yearsum['daily']): 
    plt.text(a-0.25, b+100, str(b))

# average daily amount of bikers on a week day for each year
yearsum_week_days = week_days.groupby(['year']).sum()
yearsum_week_days.drop([2011, 2017], inplace=True)
week_days_per_day = week_days.groupby(['date','year'])['total'].sum().reset_index()
count_week_days = week_days_per_day.groupby(['year'])['date'].count()
count_week_days.drop([2011, 2017], inplace=True)
yearsum_week_days['daily'] = yearsum_week_days['total'] // count_week_days

plt.plot(yearsum_week_days.index, yearsum_week_days['daily'], label='week days')
for a,b in zip(yearsum_week_days.index, yearsum_week_days['daily']): 
    plt.text(a-0.25, b+100, str(b))

# average daily amount of bikers on a weekend day for each year
yearsum_weekend_days = weekend_days.groupby(['year']).sum()
yearsum_weekend_days.drop([2011, 2017], inplace=True)
weekend_days_per_day = weekend_days.groupby(['date','year'])['total'].sum().reset_index()
count_weekend_days = weekend_days_per_day.groupby(['year'])['date'].count()
count_weekend_days.drop([2011, 2017], inplace=True)
yearsum_weekend_days['daily'] = yearsum_weekend_days['total'] // count_weekend_days

plt.plot(yearsum_weekend_days.index, yearsum_weekend_days['daily'], label='weekend days')
plt.axis([2011, 2017, 0, 8000])
for a,b in zip(yearsum_weekend_days.index, yearsum_weekend_days['daily']): 
    plt.text(a-0.25, b+100, str(b))

plt.title('Average amount of bikes at coupure')
plt.legend(loc='upper left')
plt.savefig('plots/avg_daily_bikes_each_year')