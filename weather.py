import os
import subprocess
from darksky.api import DarkSky
from darksky.types import languages, units, weather

API_KEY = os.environ.get("weather_api_key")

# Synchronous way
darksky = DarkSky(API_KEY)

countries = {
    "singapore": {
        "latitude": 1.2905,
        "longitude": 103.852
    }
}


def main():
    fc = darksky.get_forecast(
        countries["singapore"]["latitude"], countries["singapore"]["longitude"],
        extend=False,  # default `False`
        lang=languages.JAPANESE,  # default `ENGLISH`
        units=units.AUTO,  # default `auto`
        exclude=[weather.MINUTELY, weather.ALERTS]  # default `[]`
    )

    current_date = fc.currently.time.strftime("%Y年%m月%d日")
    current_hr = fc.currently.time.strftime("%H時")
    current_min = fc.currently.time.strftime("%M分")
    jp_output = f"""
    {current_date}。{current_hr}。{current_min}。
    シンガポールの今日の天気予報。
    天気。 {fc.currently.summary}。
    温度。 {fc.currently.temperature}ド。
    体感温度。 {fc.currently.apparent_temperature}ド。
    湿度。 {fc.currently.humidity * 100}パーセント。
    風。 秒速{fc.currently.wind_speed}メートル。
    """
    show_output = f"""
    {current_date} {current_hr}{current_min}
    シンガポールの今日の天気予報:
        天気: {fc.currently.summary}
        温度: {fc.currently.temperature}度
        体感温度: {fc.currently.apparent_temperature}度
        湿度: {fc.currently.humidity * 100} %
        風: {fc.currently.wind_speed} m/s
    """
    print(show_output)

    subprocess.check_output(["say", jp_output])


if __name__ == "__main__":
    main()
