import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk
import requests

# Клас WeatherServiceFacade використовується для спрощення взаємодії з веб-сервісом погоди.
class WeatherServiceFacade:
    def __init__(self, base_url):
        self.base_url = base_url

    # Приватний метод для відправки запиту до веб-сервісу.
    def _make_request(self, endpoint, city):
        try:
            url = f'{self.base_url}/{endpoint}?city={city}'
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": "Помилка під час отримання даних про погоду."}
        except Exception as e:
            return {"error": f"Виникла помилка: {e}"}

    # Метод для отримання поточної погоди для вказаного міста.
    def get_weather(self, city):
        return self._make_request("get_weather", city)

    # Метод для отримання тижневого прогнозу погоди для вказаного міста.
    def get_weekly_forecast(self, city):
        return self._make_request("get_weekly_forecast", city)

# Клас View відповідає за створення графічного інтерфейсу користувача.
class View:
    def __init__(self, root, weather_service):
        self.root = root
        self.weather_service = weather_service
        self.root.title("Погода")  # Назва вікна
        self.root.geometry("600x400")  # Розмір вікна

        self._center_window()  # Центрує вікно на екрані.

        # Створення і розміщення елементів GUI:
        self.label = self._create_label("Введіть назву міста:")
        self.entry = self._create_entry()
        self.get_weather_button = self._create_button("Отримати прогноз погоди", self.get_weather)
        self.result_label = self._create_label("")
        self.tree = self._create_treeview()

    # Метод для центрування вікна на екрані.
    def _center_window(self):
        window_width = 600
        window_height = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Метод для створення текстового напису на GUI.
    def _create_label(self, text):
        label = tk.Label(self.root, text=text)
        label.pack(pady=10)
        return label

    # Метод для створення поля для введення тексту на GUI.
    def _create_entry(self):
        entry = tk.Entry(self.root)
        entry.pack()
        return entry

    # Метод для створення кнопки на GUI.
    def _create_button(self, text, command):
        button = tk.Button(self.root, text=text, command=command)
        button.pack(pady=10)
        return button

    # Метод для створення таблиці (Treeview) на GUI.
    def _create_treeview(self):
        tree = ttk.Treeview(self.root, columns=("Дата і час", "Температура (°C)", "Опис"), show="headings")
        tree.heading("#1", text="Дата і час")
        tree.heading("#2", text="Температура (°C)")
        tree.heading("#3", text="Опис")
        tree.pack(pady=10)
        return tree

    # Метод, який викликається при натисканні кнопки "Отримати прогноз погоди".
    def get_weather(self):
        city = self.entry.get()
        if city:
            weather_data = self.weather_service.get_weather(city)
            if "error" in weather_data:
                messagebox.showerror("Помилка", weather_data["error"])
            else:
                temperature = weather_data['main']['temp']
                description = weather_data['weather'][0]['description']
                self.result_label.config(text=f"Поточна температура: {temperature}°C, {description}")
                weekly_forecast_data = self.weather_service.get_weekly_forecast(city)
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

    # Метод для відображення тижневого прогнозу погоди в таблиці.
    def display_weekly_forecast(self, weekly_forecast_data):
        self.tree.delete(*self.tree.get_children())
        for date, data in weekly_forecast_data.items():
            date_time = date
            temperature = data['temperature']
            description = data['description']
            self.tree.insert("", "end", values=(date_time, temperature, description))

# Головна частина програми:
if __name__ == "__main__":
    root = tk.Tk()
    weather_service = WeatherServiceFacade("http://localhost:5000")  # Ініціалізація WeatherServiceFacade
    view = View(root, weather_service)  # Створення графічного інтерфейсу
    root.mainloop()  # Запуск головного цикла GUI