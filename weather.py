import os
import subprocess
from darksky.api import DarkSky
from darksky.types import languages, units, weather

API_KEY = os.environ.get("weather_api_key")

# Synchronous way
darksky = DarkSky(API_KEY)

cities = {
    "sg": {
        "lang": {
            "jp": "シンガポール",
            "en": "Singapore"
        },
        "latitude": 1.2905,
        "longitude": 103.852
    },
    "tyo": {
        "lang": {
            "jp": "東京",
            "en": "Tokyo"
        },
        "latitude": 35.6828,
        "longitude": 139.759
    }
}

languages = {
    "en": languages.ENGLISH,
    "jp": languages.JAPANESE
}

days = {
    "jp": {
        "Monday": "月曜日",
        "Tuesday": "火曜日",
        "Wednesday": "水曜日",
        "Thursday": "木曜日",
        "Friday": "金曜日",
        "Saturday": "土曜日",
        "Sunday": "日曜日"
    }
}

voice = {
    "jp": "Kyoko",
    "en": "Samantha"
}


def jpMode(fc, city, lang):
    current_date = fc.currently.time.strftime("%Y年%m月%d日")
    current_day = fc.currently.time.strftime("%A")
    current_hr = fc.currently.time.strftime("%H時")
    current_min = fc.currently.time.strftime("%M分")
    say_output = f"""
    {current_date}。{days[lang][current_day]}。{current_hr}。{current_min}。
    {cities[city]["lang"][lang]}の天気予報。
    天気。 {fc.currently.summary}。
    温度。 {fc.currently.temperature}ド。
    体感温度。 {fc.currently.apparent_temperature}ド。
    湿度。 {fc.currently.humidity * 100:.2f}パーセント。
    風。 秒速{fc.currently.wind_speed}メートル。
    """
    show_output = f"""
    {current_date} {days[lang][current_day]} {current_hr}{current_min}
    {cities[city]["lang"][lang]}の天気予報:
        天気: {fc.currently.summary}
        温度: {fc.currently.temperature}度
        体感温度: {fc.currently.apparent_temperature}度
        湿度: {fc.currently.humidity * 100:.2f} %
        風: {fc.currently.wind_speed} m/s
    """
    return say_output, show_output


def enMode(fc, city, lang):
    current_date = fc.currently.time.strftime("%d %B, %Y")
    current_day = fc.currently.time.strftime("%A")
    current_hr = fc.currently.time.strftime("%H")
    current_min = fc.currently.time.strftime("%M")
    say_output = f"""
    {current_day}. {current_date}. at {current_hr}. {current_min}.
    Weather forecast in {cities[city]["lang"][lang]}.
    Current weather is {fc.currently.summary}.
    The temperature is {fc.currently.temperature} degree celsius.
    But it feels like {fc.currently.apparent_temperature} degree celsius.
    The humidity is {fc.currently.humidity * 100:.2f} percent.
    The wind speed is {fc.currently.wind_speed} meter per second.
    """
    show_output = f"""
    {current_day}, {current_date}, at {current_hr}:{current_min}
    Weather forecast in {cities[city]["lang"][lang]}:
    Current weather is {fc.currently.summary}
    The temperature is {fc.currently.temperature}°C
    But it feels like {fc.currently.apparent_temperature}°C
    The humidity is {fc.currently.humidity * 100:.2f}%
    The wind speed is {fc.currently.wind_speed} m/s
    """
    return say_output, show_output


def main(city, lang="en"):
    fc = darksky.get_forecast(
        cities[city]["latitude"], cities[city]["longitude"],
        extend=False,  # default `False`
        lang=languages[lang],  # default `ENGLISH`
        units=units.AUTO,  # default `auto`
        exclude=[weather.MINUTELY, weather.ALERTS]  # default `[]`
    )
    if lang == "jp":
        say_output, show_output = jpMode(fc, city, lang)
    else:
        say_output, show_output = enMode(fc, city, "en")

    print(show_output)
    subprocess.check_output(["say", "-v", voice[lang], say_output])


if __name__ == "__main__":
    main("sg", "jp")
