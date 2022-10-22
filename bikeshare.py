import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
# Add change by refactoring branch
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:    
        city = input('Would you like to see data for Chicago, New York, or Washington?\n').lower()
        if city in CITY_DATA:
            print('\nYou selected city: {}.'.format(city.title()))
            break
        else:
            print('\nInvalid CITY selection. Please try again!!!')
            continue

    # get user input for month (all, january, february, ... , june)
    while True:
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
        month = input('\nWhich month? January, February, March, April, May, or June? Enter \'all\' for no filter.\n').lower()
        if month in months:
            print('\nYou selected month: {}.'.format(month.title()))
            break
        else:
            print('\nInvalid MONTH selection. Please try again!!!')
            continue
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
        day = input('\nWhich day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday. Enter \'all\' for no filter.\n').lower()
        if day in days:
            print('\nYou selected day: {}.'.format(day.title()))
            break
        else:
            print('\nInvalid DAY selection. Please try again!!!')
            continue

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('Most common Month:', common_month)

    # display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print('Most common Day of week:', common_day_of_week)

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('Most common Start Hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most commonly used Start Station:', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most commonly used End Station:', common_end_station)

    # display most frequent combination of start station and end station trip
    df['station_combine'] = df['Start Station'] + " - " + df['End Station']
    common_station_combine = df['station_combine'].mode()[0]
    print('Most frequent combination of Start station and End station trip:', common_station_combine)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time:', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print('Counts of User Types:\n', user_type)

    try:

        # Display counts of gender
        gender = df['Gender'].value_counts()
        print('\nCounts of Gender:\n', gender)

        # Display earliest, most recent, and most common year of birth
        earliest_yob = df['Birth Year'].min()
        print('\nEarliest year of birth:', int(earliest_yob))

        recent_yob = df['Birth Year'].max()
        print('Most recent year of birth:', int(recent_yob))

        common_yob = df['Birth Year'].mode()[0]
        print('Most common year of birth:', int(common_yob))
    except:
        print('\nWashington dataset does not contain Gender and Birth year.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def gen_data(df):
    count = 0
    while True:
        view_data = input('\nWould you like to view individual trip data? Enter yes or no.\n').lower()
        if view_data == 'yes':
            print(df.iloc[count:count+5])
            count += 5
            print('-'*40)
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        gen_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
