import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk
import requests

class View:
    def __init__(self, root):
        self.root = root
        self.root.title("Погода")
        self.root.geometry("600x400")

        window_width = 600
        window_height = 400
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.label = tk.Label(root, text="Введіть назву міста:")
        self.label.pack(pady=10)

        self.entry = tk.Entry(root)
        self.entry.pack()

        self.get_weather_button = tk.Button(root, text="Отримати прогноз погоди", command=self.get_weather)
        self.get_weather_button.pack(pady=10)

        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

        self.tree = ttk.Treeview(root, columns=("Дата і час", "Температура (°C)", "Опис"), show="headings")
        self.tree.heading("#1", text="Дата і час")
        self.tree.heading("#2", text="Температура (°C)")
        self.tree.heading("#3", text="Опис")
        self.tree.pack(pady=10)

    def get_weather(self):
        city = self.entry.get()
        if city:
            weather_data = self.fetch_weather_data(city)
            if "error" in weather_data:
                messagebox.showerror("Помилка", weather_data["error"])
            else:
                temperature = weather_data['main']['temp']
                description = weather_data['weather'][0]['description']
                self.result_label.config(text=f"Поточна температура: {temperature}°C, {description}")
                weekly_forecast_data = self.fetch_weekly_forecast_data(city)
                if "error" in weekly_forecast_data:
                    messagebox.showerror("Помилка", weekly_forecast_data["error"])
                else:
                    daily_forecast = {}
                    for item in weekly_forecast_data['list']:
                        date_time = item['dt_txt']
                        date = date_time.split()[0]
                        if date not in daily_forecast:
                            daily_forecast[date] = {
                                'temperature': item['main']['temp'],
                                'description': item['weather'][0]['description']
                            }
                    self.display_weekly_forecast(daily_forecast)
        else:
            messagebox.showwarning("Попередження", "Будь ласка, введіть назву міста")

    def fetch_weather_data(self, city):
        try:
            url = f'http://localhost:5000/get_weather?city={city}'
            response = requests.get(url)
            if response.status_code == 200:
                weather_data = response.json()
                return weather_data
            else:
                return {"error": "Помилка під час отримання даних про погоду."}
        except Exception as e:
            return {"error": f"Виникла помилка: {e}"}

    def fetch_weekly_forecast_data(self, city):
        try:
            url = f'http://localhost:5000/get_weekly_forecast?city={city}'
            response = requests.get(url)
            if response.status_code == 200:
                forecast_data = response.json()
                return forecast_data
            else:
                return {"error": "Помилка під час отримання даних про погоду."}
        except Exception as e:
            return {"error": f"Виникла помилка: {e}"}

    def display_weekly_forecast(self, weekly_forecast_data):
        self.tree.delete(*self.tree.get_children())
        for date, data in weekly_forecast_data.items():
            date_time = date
            temperature = data['temperature']
            description = data['description']
            self.tree.insert("", "end", values=(date_time, temperature, description))

if __name__ == "__main__":
    root = tk.Tk()
    view = View(root)
    root.mainloop()