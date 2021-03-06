import pandas as pnd  # importing pandas library.
import matplotlib  # importing matplotlib to be able to make charts.


def cleanup(csv_name):
    """Create a Pandas dataframe from a CSV and remove unnecessary data."""

    data_frame = pnd.read_csv(csv_name)
    # updating the data frame removing unnecessary columns with the method .drop()
    new_data_frame = data_frame.drop(
      ['Attributes', 'Supplemental Video Type', 'Device Type', 'Bookmark', 'Latest Bookmark'],
      axis=1
    )
    # we check the data types for each column in dataframe (Pandas sees them as objects-strings).
    # We convert them in Datetime and Timedelta in Pandas
    print(data_frame.dtypes)
    new_data_frame['Start Time'] = pnd.to_datetime(new_data_frame['Start Time'], utc=True)
    # check afterwards that data types have been converted
    print(new_data_frame.dtypes)
    # convert datetimes to the appropriate timezone using .tz_convert 
    # but before we need to set Start Time as rhe index .set_index()
    new_data_frame = new_data_frame.set_index('Start Time')
    new_data_frame.index = new_data_frame.index.tz_convert('Europe/London')
    # resetting the index so that Start Time is a column again
    new_data_frame =  new_data_frame.reset_index()
    print(new_data_frame.head(1))
    # Duration: converting it to a timedelta, 
    # which is a measure of time duration that pandas understands.
    new_data_frame['Duration'] = pnd.to_timedelta(new_data_frame['Duration'])
    print(new_data_frame.dtypes)

    return new_data_frame


def filtering_data(data_frame):
    """Filter "Saul" views strings by substrings in Pandas str.contains().
    
    Creates a new data frame called saul that takes from data_frame only 
    rows containing 'Better Call Saul' in the Title column.
    """

    saul = data_frame[
      data_frame['Title'].str.contains('Better Call Saul', regex=False)
    ]

    # filtering out previews by limiting it to rows
    # where the Duration valuie is greater than one minute.
    saul = saul[
      (saul['Duration'] > '0 days 00:01:00')
    ]
    print(saul.shape)

    return saul


def calculation(duration_data):
    """How much time have i spent watching Better Call Saul? .sum()"""

    time_spent = duration_data['Duration'].sum()
    print(time_spent)
    # when do I watch Better Call Saul? Using the methods '.dt.weekday' and 'dt.hour'
    # and assigning the results of calling them on Start Time to two new columns
    duration_data['weekday'] = duration_data['Start Time'].dt.weekday
    duration_data['hour'] = duration_data['Start Time'].dt.hour
    # checking that the columns were added correctly

    # plotting a chart of my viewing habits by day of the week method .Categorical()
    duration_data['weekday'] = pnd.Categorical(
      duration_data['weekday'], 
      categories=[item for item in range(0, 7)],
      ordered=True
    )
    # creating saul_by_day and counting the rows for each weekday, assigning the result to that variable
    saul_by_day = duration_data['weekday'].value_counts()
    # sorting the index using categorical, so that Monday (0) is first, Tuesday (1) is second, etc.
    saul_by_day = saul_by_day.sort_index()
    # plotting saul_by_day as a bar chart with the listed size and title
    saul_by_day.plot(
      kind='bar',
      figsize=(20,10),
      title="Saul's Episodes Watched by Day"
    )

    print(saul_by_day)

    # same as above, by hour
    duration_data['hour'] = pnd.Categorical(
      duration_data['hour'],
      categories=[item for item in range(0, 24)],
      ordered=True
    )

    saul_by_hour = duration_data['hour'].value_counts()
    saul_by_hour = saul_by_hour.sort_index()
    saul_by_hour.plot(
      kind='bar',
      figsize=(20,10),
      title="Saul's Episodes Watched by Hour"
    )

    print(saul_by_hour)
