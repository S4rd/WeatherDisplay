import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup


class WeatherApp:
    def __init__(self, master):
        self.master = master
        master.title("Weather App")
        master.configure(bg="lightblue")

        # Create city selection dropdown list
        self.city_label = tk.Label(master, text="Select a city:", font=("Helvetica", 16), fg="blue", bg="lightblue")
        self.city_label.pack(padx=10, pady=10)

        self.city_var = tk.StringVar()
        self.city_var.set("Izmir")
        self.city_options = ["Izmir", "Istanbul", "Ankara", "Bursa", "Antalya", "Diyarbakir"]
        self.city_dropdown = tk.OptionMenu(master, self.city_var, *self.city_options)
        self.city_dropdown.pack(padx=10, pady=10)

        # Create Get Weather button
        self.get_weather_button = tk.Button(master, text="Get Current Weather", command=self.get_weather_data,
                                            font=("Helvetica", 14))
        self.get_weather_button.pack(padx=10, pady=10)

        # Create Get Forecast button
        self.get_forecast_button = tk.Button(master, text="Get 3-Day Forecast", command=self.get_forecast,
                                             font=("Helvetica", 14))
        self.get_forecast_button.pack(padx=10, pady=10)

        # Create weather information display area
        self.weather_info_label = tk.Label(master, text="Weather Information:", font=("Helvetica", 16), fg="blue",
                                           bg="lightblue")
        self.weather_info_label.pack(padx=10, pady=10)

        self.weather_info_text = tk.Text(master, height=10, width=40, font=("Helvetica", 14))
        self.weather_info_text.pack(padx=10, pady=10)

    def get_weather_data(self):
        try:
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
        except requests.exceptions.ConnectionError:
            self.weather_info_text.delete(1.0, tk.END)
            self.weather_info_text.insert(tk.END, "Error: No internet connection")

    def get_forecast(self):
        try:
            # Get entered city from search box
            city = self.city_var.get()
            city = city.replace(" ", "-")

            # Get location key for entered city
            location_keys = {
                "Ankara": "316938",
                "Izmir": "318290",
                "Istanbul": "318251",
                "Antalya": "316939",
                "Bursa": "317350"
            }
            location_key = location_keys[city]

            # Send request to AccuWeather API to get 5-day forecast for entered city
            url = f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{location_key}?apikey=A4AwSvoRGPFyj8Oa2cC5w2HqchdSIDcT"
            response = requests.get(url)
            data = response.json()

            # Extract 3-day forecast data from response
            forecast_data = data["DailyForecasts"][:3]
            forecast_strs = []
            for day_data in forecast_data:
                date_str = day_data["Date"][:10]
                min_temp = day_data["Temperature"]["Minimum"]["Value"]
                max_temp = day_data["Temperature"]["Maximum"]["Value"]
                day_str = f"{date_str}: {min_temp}°F lo - {max_temp}°F hi"
                forecast_strs.append(day_str)
            forecast_str = "\n".join(forecast_strs)

            # Update weather information display area
            weather_info = f"City: {city}\n3-Day Forecast:\n{forecast_str}"
            self.weather_info_text.delete(1.0, tk.END)
            self.weather_info_text.insert(tk.END, weather_info)
        except requests.exceptions.ConnectionError:
            self.weather_info_text.delete(1.0, tk.END)
            self.weather_info_text.insert(tk.END, "Error: No internet connection")


root = tk.Tk()
app = WeatherApp(root)
root.mainloop()
