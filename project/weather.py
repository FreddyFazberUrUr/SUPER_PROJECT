import requests
from CONSTS import API_WEATHER_KEY, WEATHER_URL


def get_weather(city):
    ret = ''
    e = ''
    try:
        response = requests.get(WEATHER_URL, params={'q': city, 'units': 'metric',
                                                     'appid': API_WEATHER_KEY, 'lang': 'ru'})
        data = response.json()
        if response.status_code == 200:
            temperature = data['main']['temp']
            temperature_comfort = data['main']['feels_like']
            weather_description = data['weather'][0]['description'].capitalize()
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']

            ret += f"Погода в городе {city}:\n"
            ret += weather_description
            ret += f"\nТемпература: {temperature}°C\n"
            ret += f"Температура по ощущениям: {temperature_comfort}°C\n"
            ret += f"Влажность: {humidity}%\n"
            ret += f"Скорость ветра: {wind_speed} м/с\n"
        else:
            e = "Город не найден. Проверьте правильность написания и попробуйте снова."

    except Exception as e:
        e = f'Невозможно получить погоду. Попробуйте снова позже. Текст ошибки: {e}'
    return ret, e


if __name__ == "__main__":
    cit = input("Введите название города: ")
    print(get_weather(cit))
