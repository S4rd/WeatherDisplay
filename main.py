import requests
from bs4 import BeautifulSoup

city = input("Enter the name of the city: ")
url = f"https://www.weather-forecast.com/locations/{city}/forecasts/latest"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

temp_div = soup.find("div", class_="b-metar-table__temperature-value temp-color3")
temp = temp_div.find("span", class_="temp").text

wind_div = soup.find("div", class_="b-metar-table__wind-detail")
wind_speed = wind_div.find("span", class_="windp").text

print(f"The current temperature in {city} is {temp}. The wind speed is {wind_speed} km/h.")