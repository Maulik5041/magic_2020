"""
Language: Python 3

    NOTE: Due to heavy file and code implementation
          logic, do not run the file directly if
          you only want to test out the approach.
          The file might take a few minutes to run
          depending upon the machine. To check the
          sample, use slicing of 2000 to 5000 value
          on lines 170 and 243. Selecting until 5000
          would cover close 700K records

************************************************************

Weather report and various analysis:

First thoughts:

  - Python provides with the csv module which
    can be used to manipulate various data
  - On opening the csv, I did not realize that
    the records have been truncated
  - Did some dry tests on the records size using
    functions from csv module and realized the
    presence of half a million records
  - With this realization I dropped the idea of
    using that module and it would not have been
    efficient enough

Second thoughts:

  - The most likely options in the arsenal of Python
    were: Pandas and NumPy
  - Although, only using Pandas could be sufficient
    in various scenarios
  - As this is more of a 'assessment' assignment, I
    have assumed that this might not require extra
    level of granularity and thus would stick to only
    Pandas
  - By no means this is the only way to solve the problem.
    But to my understanding this should be efficient enough
    to get the desired result to the best of my understanding
    of the question

*****************************************************************

Question 1: Get the lowest temperature

--> There are 2 ways of solving this problem:

   - Using the general data structure approach
     and doing all calculations manually

   - Pythonic way by utilizing Pandas module

My Approach: As this is pertaining to Python role,
             I assumed of sticking to the Pythonic
             way of solving. Although, I have briefly
             explained the approach in general way

General Approach:

  1. Convert the entire column to a list/array
  2. This list will be the value of all temperatures
  3. Thus, we will have a list as:
        [temp1, temp2, temp3, .., tempN]

  4. In the function, find the minimum value from list

  5. Using this minimum value, look-up the table for its first
      occurence. Get the pair of station_id and date

  6. Time Complexity: O(N + N + N) = O(3N)
                                   ~ O(N)

                O(N) to convert column to list
                O(N) to find the minimum
                O(N) to get the station_id and date

  7. Space Complexity: O(N) for storing the list

"""


import pandas as pd


def get_lowest_temp(complete_weather):
    """Function that returns the station id and date
       when the lowest temperature was reported"""

    # Looking up the lowest value in temperature column
    # this will return only 1 value out of multiple --> O(N)
    least_temp_value = complete_weather.nsmallest(1, "temperature_c")

    # pairing up the station id and date from the lowest temperature row
    # this needs the look-up operation, but as there is only 1 row --> O(1)
    return (least_temp_value.iloc[0, 0], least_temp_value.iloc[0, 1])


"""
**************************************************************************
Question 2: Get the station_id with highest amount of temperature
             fluctuations over all the dates

--> Similar to question 1, this could be solved generally and pythonically

My Approach: Python Pandas dataframe makes it easier to analyze the date and
              manipulate it according to the need. General approach explained
              below

General Approach:

  1. Create a dictionary with keys as all the unique station ids --> O(N)
  2. Loop over this dictionary by accessing all the temperatures
      for that particular station_id and create a list as dictionary
      values --> O(M), M = no of unique stations
  3. The dictionary will look like:

        {
         station_id_1 : [temp1, temp2, temp3, ... tempN],
         station_id_2 : [temp1, temp2, temp3, ... tempN],
         .
         .
         station_id_M : [temp1, temp2, temp3, ... tempN]
        }

  4. Create helper function that keeps track of absolute difference
      in everyday temperature in the list and keeps on summing
      these values. That will be overall fluctuation --> O(k)
                                            -- k = no of days

      i.e. temperature_list = [2, -9, 0, 12, 20, 0]
                            = 2 - (-9)
                            + 9 - 0
                            + 12 - 0
                            + 20 - 12
                            + 20 - 0
                            ----------
                            = 60

  5. Loop over the dictionary and pass the value of list of temperatures
      as parameter of helper function and keep track of maximum fluctuation
      and its corresponding station_id found yet in a local variables.
      After the end of the loop, we can directly return the station_id

  6. Time complexity: O(N + M + M*k)

                 O(N) for creating dictionary from table
                 O(M) for looping all stations and creating
                      list of temperatures
                 O(M*k) for outer loop of M stations
                        and inner loop of k days
*****************************************************************************
"""


def most_amt_fluctuation(complete_weather, all_stations):
    """Function that returns station_id of the most amount
        of fluctuated temperatures during all the dates"""

    # station_id of maximum fluctuation yet
    max_fluc_id = None

    # value of maximum fluctuation yet
    max_fluc = 0

    # looping over the dataframe by using unique station ids
    # use slice on all_stations[:5000] for sample testing of ~700K rows
    for curr_station in all_stations:

        # creating temporary dataframe for a single station_id
        temp_df = complete_weather[complete_weather["station_id"] == curr_station]

        # tracking the difference in all the temperatures in order
        local_fluctuation = temp_df["temperature_c"].diff()

        # converting the flucuated value to absolute difference
        actual_fluctuation = local_fluctuation.abs()

        # summing up the fluctuations over all the days
        total_fluctuation = actual_fluctuation.sum()

        ##################################################################
        # NOTE: The above 3 steps could be written as:                   #
        #                                                                #
        # total_fluctuation = temp_df["temperature_c"].diff().abs().sum()#
        #                                                                #
        # But have been broken down to explain properly                  #
        ##################################################################

        # check if the total fluctuation is more than the max_fluctuation
        # if the fluctuation is more, then update the station_id
        if total_fluctuation > max_fluc:
            max_fluc = total_fluctuation
            max_fluc_id = curr_station

    return max_fluc_id


"""
*********************************************************************************
Question 3: Get the station_id that experienced the most fluctuation over a range
             of dates.

My approach: This question took the maximum amount of time as I was not able
                 to exactly understand what is required here. I wanted to get a
                 very granular result but could not really understand how was the
                 question formed. But I have tried to get the result according to
                 my understanding.

             Instead of getting a granular result, I just wanted to get the station
                 for the maximum fluctuation. So, from the example given in the
                 question, I came up with a very brute logic that, for a given
                 station_id, if I can get the top 2 fluctuations and add them up,
                 I could get a rough result for that station.

                 Ex: temp         = [10, 3, 14, 0, 25, 19]
                     fluctuations = [None, 7, 11, 14, 25, 6]

                     top 2 fluctuations: 25 and 14 (0 --> 25 and 14 --> 0)
                     Thus, the total fluctuation in temperature: 25 + 14 = 39

             This logic is applied to all the station_ids and, like question 2,
             the max fluctuation value and station ids were tracked throughout
             the loop. At the end of the loop we will have the required station_id
**********************************************************************************
"""


def highest_fluc_range(complete_weather, all_stations):
    """Function that returns station_id of the most amount
        of fluctuated temperatures during all the dates"""

    # station_id of maximum fluctuation yet
    max_fluc_id = None

    # value of maximum fluctuation yet
    max_fluc = 0

    # looping over the dataframe by using unique station ids
    # use slice on all_stations[:5000] for sample testing of ~700K rows
    for curr_station in all_stations:

        # creating temporary dataframe for a single station_id
        temp_df = complete_weather[complete_weather["station_id"] == curr_station]

        # getting the fluctuation for all the temperatures of all dates
        # taking the absolute value of the fluctuation
        # selecting the top 2 largest fluctuated temperatures
        # summing them up
        local_fluctuation = (temp_df.temperature_c.diff().abs()).nlargest(2).sum()

        if local_fluctuation > max_fluc:
            max_fluc = local_fluctuation
            max_fluc_id = curr_station

    return max_fluc_id


if __name__ == '__main__':

    # converting csv to pandas dataframe
    # pandas dataframe is the csv version of Python
    weather_info = pd.read_csv('data.csv')

    # To keep a track of all station ids uniquely
    station_id_list = (weather_info.station_id.unique()).tolist()

    lowest_temp = get_lowest_temp(weather_info)
    max_fluc_station = most_amt_fluctuation(weather_info, station_id_list)
    highest_fluc_station = highest_fluc_range(weather_info, station_id_list)

    print(f'\nThe lowest temperature recorded around all the stations was\
 (station_id, date) = {lowest_temp}\n')
    print(f'The most amount of fluctuation of temperatures across all dates\
 was at station_id = {max_fluc_station}\n')
    print(f'The highest amount of fluctuated temperature ranges across all\
 stations were at station_id = {highest_fluc_station}\n')


"""
Final thoughts:

- After coming up with the solution, I have almost crossed 2 hour mark
- On re-evaluating the solution, I think I might have ended up considering
   a very memory intense approach
- In order to avoid a brute force approach of Python, I used another brute
   force from Pandas
- On top of my head, other options would have been to iterate using iteritems(),
   iterrows() or NumPy vectorization to get faster loop results
- Having thought of other seemingly better approach, I cannot think of getting
   around the fact that it is important to visit all the values of temperature
   column to get any useful insight
- My logic was to isolate the data "station_id-wise" and do the analysis on it.
   For that, I got all the unique station_ids and then performed the calculation
- So, I cannot imagine how much faster other approaches would have been
- Time complexity would have linear relation as everytime we need to iterate
   over the column, the calculation is performed by one pass itself.

      Time complexity = O(N)
      Space complexity = O(N)

- Space complexity would be O(N) due to the dataframe created. Additional space
   might be required for storing temporary dataframes
"""
