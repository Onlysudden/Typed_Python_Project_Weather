from gps_coordinates import get_gps_coordinates
from weather_api_service import get_weather
from weather_formatter import format_weather
from exceptions import ApiServiceError, CantGetCoordinates
from history import save_weather, PlainFileWeatherStorage, JSONFileWeatherStorage
from pathlib import Path

def main():
    try:
        coordinates = get_gps_coordinates()
    except CantGetCoordinates:
        print("Не удалось получить GPS координаты")
        exit(1)
    try:
        weather = get_weather(coordinates)
    except ApiServiceError:
        print(f"Не удалось получить погоду по координатам {coordinates}")
        exit(1)
    save_weather(
        weather,
        JSONFileWeatherStorage(Path.cwd() / "history.json")
    )
    print(format_weather(weather))

if __name__ == "__main__":
    main()