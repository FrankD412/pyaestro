import itertools
from string import ascii_lowercase, ascii_uppercase
from typing import Iterable


def generate_unique_upper_names(count: int) -> Iterable[str]:
    number = 0
    for length in itertools.count(1):
        for i in itertools.product(ascii_uppercase, repeat=length):
            number = number + 1
            if number > count:
                return
            yield "".join(i)


def generate_unique_lower_names(count: int) -> Iterable[str]:
    number = 0
    for length in itertools.count(1):
        for i in itertools.product(ascii_lowercase, repeat=length):
            number = number + 1
            if number > count:
                return
            yield "".join(i)
