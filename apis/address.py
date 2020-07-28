import csv
from typing import Iterator, List
from itertools import combinations

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
    return list()


def build_links(data: dict) -> List[dict]:
    return [{"name": x[0] + x[1], "distance": calc_distance(data[x[0]], data[x[1]])} for x in
            combinations(list(data.keys()), 2)]


def calc_distance(point1: List[float], point2: List[float]) -> float:
    return 1.0


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
