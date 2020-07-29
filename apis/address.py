import csv
from typing import Iterator, List
from itertools import combinations
from geopy import distance
import requests

from werkzeug.datastructures import FileStorage


class ResponseBuilder:
    def __init__(self, file: FileStorage):
        self.file = file

    def get(self) -> dict:
        csv_data = self.get_csv()
        data = self.csv_to_dict(csv_data)
        points = self.build_points(data)
        links = self.build_links(data)
        response = {"points": points, "links": links}
        return response

    def build_points(self, data: dict) -> List[dict]:
        return [{"name": name, "address": self.get_address(position[0], position[1])} for name, position in data.items()]

    @staticmethod
    def get_address(latitude: str, longitude: str) -> str:
        url = f"http://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/reverseGeocode?location={longitude}%2C{latitude}&langCode=en&outSR=&forStorage=false&f=json"
        address = requests.get(url).json()["address"]
        return address["LongLabel"] or address["PlaceName"]

    def build_links(self, data: dict) -> List[dict]:
        return [
            {
                "name": key_combination[0] + key_combination[1],
                "distance": self.calc_distance(data[key_combination[0]], data[key_combination[1]])
            }
            for key_combination in combinations(list(data.keys()), 2)
        ]

    @staticmethod
    def calc_distance(point1: List[float], point2: List[float]) -> float:
        return int(distance.geodesic(point1, point2, ellipsoid="WGS-84").km * 10) / 10

    def get_csv(self) -> Iterator:
        content = self.file.stream.read().decode('utf-8').split("\n")
        csv_data = csv.reader(content)
        next(csv_data)
        return csv_data

    @staticmethod
    def csv_to_dict(csv_data: Iterator) -> dict:
        data = dict()
        for row in csv_data:
            if row:
                data[row[0]] = [row[1], row[2]]
        return data
