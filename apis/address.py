import csv
from typing import Iterator, List
from itertools import combinations
from geopy import distance
import requests

from werkzeug.datastructures import FileStorage


# TODO: As class please
def addresses_response(file: FileStorage) -> dict:
    csv_data = get_csv(file)
    data = csv_to_dict(csv_data)
    points = build_points(data)
    links = build_links(data)
    response = {"points": points, "links": links}
    return response


def build_points(data: dict) -> List[dict]:
    return [{"name": name, "address": get_address(position[0], position[1])} for name, position in data.items()]


def get_address(latitude: str, longitude: str) -> str:
    url = f"http://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/reverseGeocode?location={longitude}%2C{latitude}&langCode=en&outSR=&forStorage=false&f=json"
    address = requests.get(url).json()["address"]
    return address["LongLabel"] or address["PlaceName"]


def build_links(data: dict) -> List[dict]:
    return [
        {
            "name": key_combination[0] + key_combination[1],
            "distance": calc_distance(data[key_combination[0]], data[key_combination[1]])
        }
        for key_combination in combinations(list(data.keys()), 2)
    ]


def calc_distance(point1: List[float], point2: List[float]) -> float:
    return int(distance.geodesic(point1, point2, ellipsoid="WGS-84").km * 10) / 10


def get_csv(file: FileStorage) -> Iterator:
    content = file.stream.read().decode('utf-8').split("\n")
    csv_data = csv.reader(content)
    next(csv_data)
    return csv_data


def csv_to_dict(csv_data: Iterator) -> dict:
    data = dict()
    for row in csv_data:
        if row:
            data[row[0]] = [row[1], row[2]]
    return data
