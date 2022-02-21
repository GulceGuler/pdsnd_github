import time
import pandas as pd
import numpy as np
import datetime 

#Defining the variables for reading the files

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#Listing months and days 
months = ['all','january','february','march','april','may','june']

days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
   
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs 
           
    city = input ('Dear user please enter one of the city names (New York City, Chicago, Wshington): ').lower()
    
    #handles invalid loops by accpeting only 3 city names and makes in case insensitive. This is done for all inputs
    while city not in ['chicago','new york city','washington']:
        city = input ('Please enter the name of the city among Chicago, New York City and Washington: ').lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    
    month = input ('Please enter the desired month from January to June: ').lower()
    
    while month not in ['all','january','february','march','april','may','june']:
        month = input ('Please enter the desired month from january to june: ').lower()
    
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    
    day = input ('Please enter the desired day: ').lower()
    
    while day not in ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']:
        day = input ('Please enter the desired day: ')
    
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
    csv_name = city.replace(" ", "_") + '.csv'
    
    df = pd.read_csv(csv_name , header = 0, sep = ',')
    
    df['Start Time'] = pd.to_datetime(df['Start Time'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    # filtering the data according to the inputs given by the user
    if months.index(month) != 0:
        df = df[df['Start Time'].dt.month == months.index(month)]
    if days.index(day) != 7:
        df = df[df['Start Time'].dt.weekday == days.index(day)]
    """
    for i in range(len(city_data)):
        start_time = datetime.datetime.strptime(city_data.loc[i,'Start Time'],'%Y-%m-%d %H:%M:%S')
        if start_time.month == months.index(month) or months.index(month) == 0:
            if start_time.weekday() == days.index(day) or days.index(day) == 7 :
                df.append(city_data.loc[i])
    """
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
  
    # df[df['Start Time'].dt.month == months.index(month)]
    df.groupby(df['Start Time'].dt.month)
    
    
    # TO DO: display the most common month
    # months[max(month_counts, key=month_counts.get)]
    df_month_sizes = df.groupby(pd.Grouper(key='Start Time', sort= True, freq='M')).size().to_frame('size')
    df_max_month = df_month_sizes['size'].idxmax().month
    
    print("The most common month is: " + months[df_max_month])
    
    # TO DO: display the most common day of week
    df_day_sizes = df.groupby(df['Start Time'].dt.weekday_name).size().to_frame('size')
    df_max_day = df_day_sizes['size'].idxmax()
    
    print("The most common day is: " + df_max_day)

    # TO DO: display the most common start hour
    df_hour_sizes = df.groupby(df['Start Time'].dt.hour).size().to_frame('size')
    df_max_hour = df_hour_sizes['size'].idxmax()   


    print("The most common hour is: " + str(df_max_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    # TO DO: display most commonly used start station
    
    df_startstation_sizes = df.groupby(df['Start Station']).size().to_frame('size')
    df_max_startstation = df_startstation_sizes['size'].idxmax()


    print("The most commonly used start station is: " + df_max_startstation)
    
    
    # TO DO: display most commonly used end station
          
    df_endstation_sizes = df.groupby(df['End Station']).size().to_frame('size')
    df_max_endstation = df_endstation_sizes['size'].idxmax()
    
    print("The most commonly used end station is: " + df_max_endstation)

    # TO DO: display most frequent combination of start station and end station trip
    
    df_most_common_trip = df.groupby(['Start Station','End Station']).size().to_frame('size')
    df_max_trip = df_most_common_trip ['size'].idxmax()
    
    print("The most frequent combination of start station and end station trip is: " + str(df_max_trip) )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
   
 
    # TO DO: display total travel time
    
    print("The total travel time in seconds is: " + str(round(df['Trip Duration'].sum())))

    # TO DO: display mean travel time
    print("The mean travel time is: " + str(round(df['Trip Duration'].mean())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    
    print("The number of user types is: " + str(df.groupby(df['User Type']).size().to_frame('count')))
                                                
    # TO DO: Display counts of gender
    if "Gender" in df:
        print("The number of people in each gender is: " + str(df.groupby(df['Gender']).size().to_frame('count')))
    else:
        print("Gender data is not available in this data set")
    # TO DO: Display earliest, most recent, and most common year of birth
    
    if "Birth Year" in df:
        print("The earliest birth year is: " + str(int(df['Birth Year'].min())))
        print("The most recent birth year is: " + str(int(df['Birth Year'].max())))
        
        df_year_sizes = df.groupby(df['Birth Year']).size().to_frame('size')
        df_max_year = df_year_sizes['size'].idxmax()
        print("The most common year of birth is: " + str(int(df_max_year)))
    else:
        print("birth year data is not available in this dataset")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """ Your docstring here """
    i = 0
    raw = input("Would you like to see the 5 rows of the data?\n").lower() # TO DO: convert the user input to lower case using lower() function
    pd.set_option('display.max_columns',200)

    while True:            
        if raw == 'no':
            break
        elif raw == 'yes':
            j = i+5
            if j >= df.size:
                j = df.size-1
            
            print(df.iloc[i:j]) # TO DO: appropriately subset/slice your dataframe to display next five rows
            raw = input("Do you want to continue seeing the data?\n").lower() # TO DO: convert the user input to lower case using lower() function
            i += 5
        else:
            raw = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
