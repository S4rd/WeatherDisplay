import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup


class WeatherApp:
    def __init__(self, master):
        self.master = master
        master.title("Weather App")

        # Create city selection search box
        self.city_label = tk.Label(master, text="Enter a city:")
        self.city_label.pack()

        self.city_var = tk.StringVar()
        self.city_entry = tk.Entry(master, textvariable=self.city_var)
        self.city_entry.pack()

        # Create Get Weather button
        self.get_weather_button = tk.Button(master, text="Get Weather", command=self.get_weather_data)
        self.get_weather_button.pack()

        # Create weather information display area
        self.weather_info_label = tk.Label(master, text="Weather Information:")
        self.weather_info_label.pack()

        self.weather_info_text = tk.Text(master, height=10, width=40)
        self.weather_info_text.pack()

        # Create temperature unit toggle button
        self.temp_unit_var = tk.StringVar(value="Celsius")
        self.temp_unit_button = tk.Button(master, textvariable=self.temp_unit_var, command=self.toggle_temp_unit)
        self.temp_unit_button.pack()

    def get_weather_data(self):
        # Get entered city from search box
        city = self.city_var.get()
        city = city.replace(" ", "-")

        # Send request to weather website to get weather data for entered city
        url = f"https://www.weather-forecast.com/locations/{city}/forecasts/latest"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract weather data from response
        temp_div = soup.find("div", class_="b-metar-table__temperature")
        temp = float(temp_div.find("span", class_="temp").text)

        wind_div = soup.find("div", class_="b-metar-table__wind-detail")
        wind_speed = float(wind_div.find("span", class_="windp").text)

        # Convert temperature to Fahrenheit if necessary
        if self.temp_unit_var.get() == "Fahrenheit":
            temp_fahrenheit = temp * 9 / 5 + 32
            temp_str = f"{temp_fahrenheit:.1f}°F"
        else:
            temp_str = f"{temp:.1f}°C"

        # Update weather information display area
        weather_info = f"City: {city}\nTemperature: {temp_str}\nWind Speed: {wind_speed} km/h"
        self.weather_info_text.delete(1.0, tk.END)
        self.weather_info_text.insert(tk.END, weather_info)

    def toggle_temp_unit(self):
        # Toggle temperature unit between Celsius and Fahrenheit
        if self.temp_unit_var.get() == "Celsius":
            self.temp_unit_var.set("Fahrenheit")
            temp_unit_str = "°F"
            conversion_factor = 9 / 5
            conversion_offset = 32
        else:
            self.temp_unit_var.set("Celsius")
            temp_unit_str = "°C"
            conversion_factor = 5 / 9
            conversion_offset = -32


root = tk.Tk()
app = WeatherApp(root)
root.mainloop()
