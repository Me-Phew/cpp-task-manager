import os.path
import re


def does_file_exist(path: str) -> bool:
    return os.path.exists(path)


def get_first_number_from_string(string):
    number = re.findall(r"\d+", string)
    return int(number[0])


class Task:
    filename: str
    number: int

    def __init__(self, filename, number):
        self.filename = filename
        self.number = number
