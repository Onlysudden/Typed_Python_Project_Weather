from dataclasses import dataclass
from subprocess import Popen, PIPE
from typing import Literal
import config
from exceptions import CantGetCoordinates

@dataclass(slots=True, frozen=True)
class Coordinates:
    latitude: float
    longitude: float

def get_gps_coordinates() -> Coordinates:
    """Returns current coordinates using MacBook GPS"""
    coordinates = _get_whereami_coordinates()
    return _round_coordinates(coordinates)

def _get_whereami_coordinates() -> Coordinates:
    whereami_output = _get_whereami_output()
    coordinates = _parse_coordinates(whereami_output)
    return coordinates

def _get_whereami_output() -> bytes:
    process = Popen(["whereami"], stdout=PIPE)
    output, err = process.communicate()
    exit_code = process.wait()
    if err is not None or exit_code != 0:
        raise CantGetCoordinates
    return output

def _parse_coordinates(whereami_output: bytes) -> Coordinates:
    try:
        output = whereami_output.decode().strip().lower().split("\n")
    except UnicodeDecodeError:
        raise CantGetCoordinates
    return Coordinates(
    latitude=_parse_coord(output, "latitude"),
    longitude=_parse_coord(output, "longitude")
    )

def _parse_coord(
        output: list[str],
        coord_type: Literal["latitude"] | Literal["longitude"]) -> float:
    for line in output:
        if line.startswith(f"{coord_type}:"):
            return _parse_float_coordinate(line.split()[1])
    else:
        raise CantGetCoordinates

def _parse_float_coordinate(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        raise CantGetCoordinates

def _round_coordinates(coordinates: Coordinates) -> Coordinates:
    if not config.USE_ROUNDED_COORDS:
        return coordinates
    return Coordinates(*map(
            lambda c: round(c, 1),
            [coordinates.latitude, coordinates.longitude]
            ))

if __name__ == "__main__":
    print(get_gps_coordinates())
"""
#First variant NamedTuple
from typing import NamedTuple

class Coordinates(NamedTuple):
    latitude: float
    longitude: float

def get_gps_coordinates() -> Coordinates:
    return Coordinates(latitude=10, longitude=20)

#Second variant Literal
from typing import Literal

def get_gps_coordinates() -> dict[Literal["longitude"] | Literal["latitude"],
float]:
    return {"longitude": 10, "latitude": 20}

print(get_gps_coordinates()["longitude"])
print(get_gps_coordinates()["longitudeRRR"]) # Тут IDE покажет ошибку!

#Third variant TypedDict
from typing import TypedDict

class Coordinates(TypedDict):
    longitude: float
    latitude: float

def get_gps_coordinates() -> Coordinates:
    return Coordinates(**{"longitude": 10, "latitude": 20})

c = Coordinates(longitude=10, latitude=20)
print(c["longitude"]) # Работает автодополнение в IDE
print(c["longitudeRRR"]) # IDE покажет ошибку

#Fourth variant Dataclass
from dataclasses import dataclass

@dataclass
class Coordinates:
    longitude: float
    latitude: float

def get_gps_coordinates() -> Coordinates:
    return Coordinates(10, 20)

print(get_gps_coordinates().latitude) # Автодополнение IDE для атрибута
print(get_gps_coordinates().latitudeRRR) # IDE подсветит опечатку
"""