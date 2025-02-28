import requests


# DSC 510
# Week 12
# 12.1 Programming Final
# Author: Jonathan Leeper
# 03/02/2024


def main():
    # Created user_input for while loop for program to continue to execute, and api key.
    api_key = '24fe17da51a463c39d322d689379b551'
    user_input = ''
    # try block for getting access to OpenWeatherMap.
    try:
        requests.get("https://api.openweathermap.org")
        print("Connection successful!")
    except requests.exceptions.HTTPError:
        print("HTTP Error. Ending Program.")
        user_input = 'quit'
    except requests.exceptions.ConnectionError:
        print("Error connecting to the website. Ending program.")
        user_input = 'quit'
    except requests.exceptions.Timeout:
        print("Timeout error. Ending program.")
        user_input = 'quit'
    except requests.exceptions.RequestException:
        print("Something is causing the website to not connect. Ending program.")
        user_input = 'quit'
    # creating while loop while user_input does not equal quit
    while user_input != 'quit':
        user_input = input("\nWhat is the city or zip code of the location you'd like to see? "
                           "Type 'quit' to end program: ").lower()
        # If user_input is a digit, try for zip code
        if user_input.isdigit():
            response = requests.get('http://api.openweathermap.org/geo/1.0/zip?zip='
                                    + user_input + ',US&appid=' + api_key)

            try:
                # This will try to call from the user input as a zip, if it does not work, will return keyError.
                lat = str(response.json()['lat'])
                lon = str(response.json()['lon'])
            except KeyError:
                print("Sorry, you didn't correctly set a city or zip.")
                continue

        else:
            # If user_input is not an int, will try city name
            if user_input == 'quit':
                continue
            state = input("please enter the two character State Code (e.g. FL) for the city: ")
            if len(state) != 2:
                print("You need to enter a two character state code. Please try again.")
                continue
            response_string = ('https://api.openweathermap.org/data/2.5/weather?q='
                               + user_input + ',' + state + ',US&appid=' + api_key)
            response = requests.get(response_string)

            try:
                # This will try to call from user input, if it does not work, will return keyError.
                lat = str(response.json()['coord']['lat'])
                lon = str(response.json()['coord']['lon'])
            except KeyError:
                # Removes redundant message in console.
                if user_input == 'quit':
                    continue
                else:
                    print("Sorry, you didn't correctly set a city or zip, or could not find city. Try again.")
                    continue
                    
        # sets city name, weather_string, and the weather_response
        city = response.json()['name']

        # Create new user_input to choose Celsius, Fahrenheit, or Kelvin. Calls the print function.
        user_input2 = input("Would you like Celsius, Fahrenheit, or Kelvin? Please type 'C', 'F', or 'K': ").lower()
        while user_input2 != 'quit':

            if user_input2 == 'c':
                weather_string = ('https://api.openweathermap.org/data/2.5/weather?lat=' + lat
                                  + '&lon=' + lon + '&appid=' + api_key + '&units=metric')
                weather_response = requests.get(weather_string)
                print_weather(weather_response, city)
                user_input2 = 'quit'

            elif user_input2 == 'f':
                weather_string = ('https://api.openweathermap.org/data/2.5/weather?lat=' + lat
                                  + '&lon=' + lon + '&appid=' + api_key + '&units=imperial')
                weather_response = requests.get(weather_string)
                print_weather(weather_response, city)
                user_input2 = 'quit'

            elif user_input2 == 'k':
                weather_string = ('https://api.openweathermap.org/data/2.5/weather?lat=' + lat
                                  + '&lon=' + lon + '&appid=' + api_key)
                weather_response = requests.get(weather_string)
                print_weather(weather_response, city)
                user_input2 = 'quit'

            elif user_input2 == 'quit':
                continue

            else:
                user_input2 = input("please type 'C', 'F', or 'K', or 'quit' to end program: ").lower()


def print_weather(weather_response, city):
    # This calls each of the needed responses from the weather_response
    temp = weather_response.json()['main']['temp']
    feel = weather_response.json()['main']['feels_like']
    temp_min = weather_response.json()['main']['temp_min']
    temp_max = weather_response.json()['main']['temp_max']
    pressure = weather_response.json()['main']['pressure']
    humidity = weather_response.json()['main']['humidity']
    description = weather_response.json()['weather'][0]['description']

    # Prints the readings.
    print("\nFahrenheit Readings: "
          "\nCity: ", city,
          "\nTemperature:", int(round(temp)),
          "\nFeels Like:", int(round(feel)),
          "\nMin:", int(round(temp_min)),
          "\nMax:", int(round(temp_max)),
          "\nPressure:", pressure,
          "\nHumidity:", humidity,
          "\nDescription:", description)


if __name__ == '__main__':
    main()

# Change#:32
# Changes Made: Correctly used try block for KeyError
# Date of Change: 03/02/24
# Author: Jonathan Leeper
# Change approved by: Jonathan Leeper
# Date moved to production: 03/02/24
