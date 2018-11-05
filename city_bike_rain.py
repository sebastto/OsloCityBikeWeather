"""
Credit to http://nbviewer.jupyter.org/github/UiO-INF3331/UiO-INF3331.github.io/blob/master/lectures/11_pandas/Pandas.ipynb
for code to extract data about the city bikes
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

# Load weather data
weather_df = pd.read_html('weather.html', parse_dates=['date'])[
    0][['date', 'mmPrecipitation']]
weather_df = weather_df[weather_df['date'].dt.month == 9]
weather_df = weather_df[weather_df['date'].dt.year == 2018]
weather_df = weather_df.reset_index(drop=True)


# Load biking data
bike_stats_sep_oct = pd.read_csv('trips-2018-september.csv',
                                 sep=',',
                                 parse_dates=['Start time', 'End time'])


# Load station data
station_json = json.load(open('stations.json', 'r'))['stations']
stations = pd.io.json.json_normalize(station_json)

stations = stations.set_index('id')
stations = stations.drop(["bounds", "subtitle"], axis=1)

# Merge biking and station data
merged_bike_stats = pd.merge(bike_stats_sep_oct, stations,
                             how='left', left_on="Start station", right_index=True)
merged_bike_stats2 = pd.merge(merged_bike_stats, stations, how='left', left_on="End station",
                              right_index=True, suffixes=("_start", "_end"))


# Find the most busy stations
busy_station = merged_bike_stats2['Start station'].value_counts()[:5]
ak_plass_stats = merged_bike_stats[merged_bike_stats["Start station"]
                                   == busy_station.index[0]]

# Resample trips
resampled_trips = pd.DataFrame({"Counter": 1},
                               index=ak_plass_stats["Start time"])
resampled_trips = resampled_trips.resample('30T').sum()

# Plot results
ax = resampled_trips.loc["2018-9-01 04:00:00":
                         "2018-09-30 23:59:59"].plot(y=['Counter'])
weather_df.plot(x='date', y='mmPrecipitation', ax=ax)
plt.title("Weather in Oslo and usage of city bikes, Sept. 2018")
plt.tight_layout()
plt.show()
