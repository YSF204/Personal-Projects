import time 
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
 
######## Shortcuts ########


CITY_SHORTCUTS = {
    'ch': 'chicago',
    'nyc': 'new york city',
    'wt': 'washington'
}

DAY_SHORTCUTS = {
    'm': 'monday',
    'tu': 'tuesday',
    'w': 'wednesday',
    'th': 'thursday',
    'f': 'friday',
    'sa': 'saturday',
    'su': 'sunday'
}

MONTH_SHORTCUTS = {
    'jan': 'january',
    'feb': 'february',
    'mar': 'march',
    'apr': 'april',
    'may': 'may',  
    'jun': 'june'
}

######## Shortcuts ########

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    while True:
        city = input("Please enter the city (chicago/ch, new york city/nyc, washington/wt): ").lower()
        if city in CITY_SHORTCUTS:
            city = CITY_SHORTCUTS[city]
        if city in CITY_DATA:
            break
        else:
            print("Invalid input. Please try again.")

    month = 'all'
    day = 'all'

    while True:
        filter = input("Would you like to filter the data by month, day, both, or not at all? (Type 'none' for no filter): ").lower()
        if filter in ['month', 'day', 'both', 'none']:
            break
        else:
            print("Invalid input. Please try again.")

    if filter == 'month' or filter == 'both':
        while True:
            month = input("Which month - January/jan, February/feb, March/mar, April/apr, May, or June/jun? ").lower()

            if month in MONTH_SHORTCUTS:
                month = MONTH_SHORTCUTS[month]
            if month in ['january', 'february', 'march', 'april', 'may', 'june']:
                break
            else:
                print("Invalid input. Try again.")

    if filter == 'day' or filter == 'both':
        while True:
            day = input("Which day (monday/m, tuesday/tu, wednesday/w, thursday/th, friday/f, saturday/sa, sunday/su)? ").lower()
            if day in DAY_SHORTCUTS:
                day = DAY_SHORTCUTS[day]
            if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                break
            else:
                print("Invalid input. Try again.")

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    """
    try:
        df = pd.read_csv(CITY_DATA[city])
        
        data_array = df.values
        print("\nDataset Information:")
        print(f"Data type: {data_array.dtype}")
        print(f"Dataset shape: {data_array.shape}")
        print(f"Number of dimensions: {data_array.ndim}")
        print(f"Total elements: {data_array.size}\n")

        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['month'] = df['Start Time'].dt.month_name().str.lower()
        df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()

        if month != 'all':
            df = df[df['month'] == month]

        if day != 'all':
            df = df[df['day_of_week'] == day]
            
        return df

    except FileNotFoundError:
        print(f"Error: The file for {city} could not be found.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: The file for {city} is empty.")
        return None

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    
    month_counts = df.groupby('month').size()
    most_common_month = month_counts.loc[month_counts == month_counts.max()].index[0]
    print(f"Most common month: {most_common_month.title()}")


    day_counts = df.groupby('day_of_week').size()
    most_common_day = day_counts.loc[day_counts == day_counts.max()].index[0]
    print(f"Most common day of week: {most_common_day.title()}")


    df['hour'] = df['Start Time'].dt.hour
    hour_counts = df.groupby('hour').size()
    most_common_hour = hour_counts.loc[hour_counts == hour_counts.max()].index[0]
    
    if most_common_hour == 0:
        formatted_hour = "12 AM"
    elif most_common_hour < 12:
        formatted_hour = f"{most_common_hour} AM"
    elif most_common_hour == 12:
        formatted_hour = "12 PM"
    else:
        formatted_hour = f"{most_common_hour - 12} PM"
        
    print(f"Most common start hour: {formatted_hour}")

    duration = round(time.time() - start_time, 4)
    print(f"\nThis took {duration} seconds.")
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    
    start_station_counts = df.groupby('Start Station').size()
    most_common_start = start_station_counts.loc[start_station_counts == start_station_counts.max()]

    print(f"Most common start station: {most_common_start.index[0]}")
    print(f"Count: {most_common_start.values[0]} trips")


    end_station_counts = df.groupby('End Station').size()
    most_common_end = end_station_counts.loc[end_station_counts == end_station_counts.max()]
    print(f"\nMost common end station: {most_common_end.index[0]}")
    print(f"Count: {most_common_end.values[0]} trips")


    trip_counts = df.groupby(['Start Station', 'End Station']).size()

    most_common_trip = trip_counts.loc[trip_counts == trip_counts.max()]
    
    
    common_start, common_end = most_common_trip.index[0]

    print(f"\nMost frequent trip:")
    print(f"From: {common_start}")
    print(f"To: {common_end}")
    print(f"Count: {most_common_trip.values[0]} trips")

    duration = round(time.time() - start_time, 4)

    print(f"\nThis took {duration} seconds.")
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    
    duration_array = df['Trip Duration'].to_numpy()
    
    total_duration = np.sum(duration_array)
    mean_duration = np.mean(duration_array)
    
    total_seconds = int(total_duration)
    days = total_seconds // (24 * 3600)
    remaining_seconds = total_seconds % (24 * 3600)
    
    hours = remaining_seconds // 3600
    remaining_seconds = remaining_seconds % 3600
    
    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60
    
    print("Total travel time:")
    if days > 0:
        print(f"- {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds")
    elif hours > 0:
        print(f"- {hours} hours, {minutes} minutes, and {seconds} seconds")
    else:
        print(f"- {minutes} minutes and {seconds} seconds")

    avg_seconds = int(mean_duration)
    avg_hours = avg_seconds // 3600
    remaining_seconds = avg_seconds % 3600
    avg_minutes = remaining_seconds // 60
    avg_seconds = remaining_seconds % 60
    
    print("\nAverage travel time:")
    if avg_hours > 0:
        print(f"- {avg_hours} hours, {avg_minutes} minutes, and {avg_seconds} seconds")
    else:
        print(f"- {avg_minutes} minutes and {avg_seconds} seconds")

    print("\nTrip Duration Statistics:")
    print(f"Standard Deviation: {round(np.std(duration_array))} seconds")
    print(f"Median Duration: {round(np.median(duration_array))} seconds")
    print(f"25th percentile: {round(np.percentile(duration_array, 25))} seconds")
    print(f"75th percentile: {round(np.percentile(duration_array, 75))} seconds")

    duration = round(time.time() - start_time, 4)
    print(f"\nThis took {duration} seconds.")
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    
    df['User Type'] = df['User Type'].fillna('Not Specified')
    user_type_stats = df['User Type'].value_counts()
    print('User Types:')
    for user_type, count in user_type_stats.items():
        print(f"- {user_type}: {count}")
    print()

    if 'Gender' in df:
        df['Gender'] = df['Gender'].fillna('Not Specified')
        gender_stats = df['Gender'].value_counts()
        print('Gender Distribution:')
        for gender, count in gender_stats.items():
            print(f"- {gender}: {count}")
        print()

    if 'Birth Year' in df:
        birth_years = df['Birth Year'].dropna()
        if not birth_years.empty:
            print('Birth Year Statistics:')
            print(f"- Earliest: {round(birth_years.min())}")
            print(f"- Most Recent: {round(birth_years.max())}")
            print(f"- Most Common: {round(birth_years.mode()[0])}")
            print(f"- Average Year: {round(birth_years.mean(), 1)}")
        else:
            print('No birth year data available')
        print()

    print(f"\nThis took {round(time.time() - start_time, 4)} seconds.")
    print('-'*40)

def display_raw_data(df):
    """Displays raw data 5 rows at a time."""
    start = 0
    
    while True:

        show_data = input('\nWould you like to see 5 rows of raw data? Enter yes/y or no/n.\n').lower()
        
        if show_data not in ['yes', 'y']:
            break
            
        print('\nDisplaying 5 rows of raw data:\n')

        print(df.iloc[start:start + 5])


        print('\n' + '-'*40)
        
        start += 5
        if start >= len(df):
            print("\nNo more data to display.")
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        if df is not None:  


            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            display_raw_data(df)  

        restart = input('\nWould you like to restart? Enter yes/y or no/n.\n').lower()
        if restart not in ['yes', 'y']:
            break

if __name__ == "__main__":
	main()
