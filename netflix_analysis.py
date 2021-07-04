import pandas as pnd  # importing pandas library.
import matplotlib  # importing matplotlib to be able to make charts.


# creating a table with data from csv through pandas
data_frame = pnd.read_csv('ViewingActivity.csv')
# updating the data frame removing unnecessary columns with the method .drop()
new_data_frame = data_frame.drop(
  ['Attributes', 'Supplemental Video Type', 'Device Type', 'Bookmark', 'Latest Bookmark'],
  axis=1
)
# we check the data types for each column in dataframe (Pandas sees them as objects-strings). We convert them in Datetime and Timedelta in Pandas
print(data_frame.dtypes)
data_frame['Start Time'] = pnd.to_datetime(data_frame['Start Time'], utc=True)
# check afterwards that data types have been converted
print(data_frame.dtypes)
# convert datetimes to the appropriate timezone using .tz_convert 
# but before we need to set Start Time as rhe index .set_index()
data_frame = data_frame.set_index('Start Time')
data_frame.index = data_frame.index.tz_convert('Europe/London')
# resetting the index so that Start Time is a column again
data_frame =  data_frame.reset_index()
print(data_frame.head(1))
# Duration: converting it to a timedelta, 
# which is a measure of time duration that pandas understands.
data_frame['Duration'] = pnd.to_timedelta(data_frame['Duration'])
print(data_frame.dtypes)


# filtering Better Call Saul views strings by substrings in Pandas str.contains()
# creating a new data frames called saul that takes from data_frame only 
# rows containing 'Better Call Saul' in the Title column
saul = data_frame[
  data_frame['Title'].str.contains('Better Call Saul', regex=False)
]
print(saul.shape)
# filtering out previews by limiting it to rows
# where the Duration valuie is greater than one minute.
saul = saul[
  (saul['Duration'] > '0 days 00:01:00')
]
print(saul.shape)
# how much time have i spent watching Better Call Saul? .sum()
time_spent = saul['Duration'].sum()
print(time_spent)
# when do I watch Better Call Saul? Using the methods '.dt.weekday' and 'dt.hour'
# and assigning the results of calling them on Start Time to two new columns
saul['weekday'] = saul['Start Time'].dt.weekday
saul['hour'] = saul['Start Time'].dt.hour
# checking that the columns were added correctly
print(saul.shape)
print(saul.head(10))


# plotting a chart of my viewing habits by day of the week method .Categorical()
saul['weekday'] = pnd.Categorical(
  saul['weekday'], 
  categories=[item for item in range(0, 7)],
  ordered=True
)
# creating saul_by_day and counting the rows for each weekday, assigning the result to that variable
saul_by_day = saul['weekday'].value_counts()
# sorting the index using categorical, so that Monday (0) is first, Tuesday (1) is second, etc.
saul_by_day = saul_by_day.sort_index()
# plotting saul_by_day as a bar chart with the listed size and title
saul_by_day.plot(
  kind='bar',
  figsize=(20,10),
  title="Saul's Episodes Watched by Day"
)


# same as above, by hour
saul['hour'] = pnd.Categorical(
  saul['hour'],
  categories=[item for item in range(0, 24)],
  ordered=True
)

saul_by_hour = saul['hour'].value_counts()
saul_by_hour = saul_by_hour.sort_index()
saul_by_hour.plot(
  kind='bar',
  figsize=(20,10),
  title="Saul's Episodes Watched by Hour"
)
