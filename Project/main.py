import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup


class WeatherApp:
    def __init__(self, master):
        self.master = master
        master.title("Weather App")



        master.configure(bg="lightblue")

        # Create city selection search box
        self.city_label = tk.Label(master, text="Enter a city:", font=("Helvetica", 16), fg="blue", bg="lightblue")
        self.city_label.pack(padx=10, pady=10)

        self.city_var = tk.StringVar()
        self.city_entry = tk.Entry(master, textvariable=self.city_var, font=("Helvetica", 14))
        self.city_entry.pack(padx=10, pady=10)

        # Create Get Weather button
        self.get_weather_button = tk.Button(master, text="Get Weather", command=self.get_weather_data,
                                            font=("Helvetica", 14))
        self.get_weather_button.pack(padx=10, pady=10)

        # Create weather information display area
        self.weather_info_label = tk.Label(master, text="Weather Information:", font=("Helvetica", 16), fg="blue",
                                           bg="lightblue")
        self.weather_info_label.pack(padx=10, pady=10)

        self.weather_info_text = tk.Text(master, height=10, width=40, font=("Helvetica", 14))
        self.weather_info_text.pack(padx=10, pady=10)

        # Create temperature unit toggle button
        self.temp_unit_var = tk.StringVar(value="Celsius")
        self.temp_unit_button = tk.Button(master, textvariable=self.temp_unit_var, command=self.toggle_temp_unit,
                                          font=("Helvetica", 14), bg="yellow", activebackground="green")
        self.temp_unit_button.pack(padx=10, pady=10)

    def get_weather_data(self):
        # Get entered city from search box
        city = self.city_var.get()
        city = city.replace(" ", "-")

        # Send request to weather website to get weather data for entered city
        url = f"https://www.weather-forecast.com/locations/{city}/forecasts/latest"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract weather data from response
        temp_td = soup.find("td", class_="b-metar-table__temperature")
        temp_div = temp_td.find("div", class_="b-metar-table__temperature-value")
        temp = float(temp_div.find("span", class_="temp").text)

        wind_div = soup.find("div", class_="b-metar-table__wind-detail")
        wind_speed = float(wind_div.find("span", class_="windp").text)

        # Convert temperature to Fahrenheit if necessary
        if self.temp_unit_var.get() == "Fahrenheit":
            temp_fahrenheit = temp * 9 / 5 + 32
            temp_str = f"{temp_fahrenheit:.1f}°F"
        else:
            temp_str = f"{temp:.1f}°C"

        # Determine temperature icon
        if temp < 10:
            temp_icon = "❄️"
        elif temp < 25:
            temp_icon = "☀️"
        else:
            temp_icon = "🔥"

        # Determine wind speed icon
        if wind_speed < 5:
            wind_speed_icon = "🍃"
        elif wind_speed < 15:
            wind_speed_icon = "🌬️"
        else:
            wind_speed_icon = "💨"

        # Update weather information display area
        weather_info = f"City: {city}\nTemperature: {temp_str} {temp_icon}\nWind Speed: {wind_speed} km/h {wind_speed_icon}"
        self.weather_info_text.delete(1.0, tk.END)
        self.weather_info_text.insert(tk.END, weather_info)

    def toggle_temp_unit(self):
        # Toggle temperature unit between Celsius and Fahrenheit
        if self.temp_unit_var.get() == "Celsius":
            self.temp_unit_var.set("Fahrenheit")
            self.temp_unit_button.configure(bg="green", activebackground="yellow")
        else:
            self.temp_unit_var.set("Celsius")
            self.temp_unit_button.configure(bg="yellow", activebackground="green")

        # Update weather information display
        self.get_weather_data()

root = tk.Tk()
app = WeatherApp(root)
root.mainloop()
