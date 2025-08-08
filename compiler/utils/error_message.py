from dataclasses import dataclass
from typing import List


@dataclass
class Error:
    error_description: str
    line_number: int
    wrong_char_index: int


@dataclass
class ErrorMessage:
    errors: List[str]

    def print(self):
        pass
