from re import finditer
from collections import OrderedDict
from mmap import mmap, ACCESS_READ, ACCESS_WRITE
from argparse import ArgumentTypeError
from prompt_toolkit.validation import Validator, ValidationError

def get_strings(min_length: int, binary: bytes) -> dict:
    strings = {}
    for match in finditer(rf"[\n -~]{{{min_length},}}".encode(), binary):
        strings.setdefault(match.group(), []).append(match.start())
    return strings
def get_strings_from_file(min_length: int, fileno: int) -> dict:
    with mmap(fileno, 0, access=ACCESS_READ) as mm:
        return get_strings(min_length, mm)
def get_sorted_strings_from_file(min_length: int, fileno: int) -> OrderedDict:
    return OrderedDict(sorted(get_strings_from_file(min_length, fileno).items()))

def print_ordered_strings(min_length: int, binary: bytes, radix: str = None, sep: str = None) -> None:
    radix_format = f"{{:{radix}}} " if radix else ""
    print(
        *(radix_format.format(match.start()) + match.group().decode()
            for match in finditer(rf"[\n -~]{{{min_length},}}".encode(), binary)),
        sep=sep if sep is not None else '\n'
    )
def print_ordered_strings_from_file(min_length: int, fileno: int, radix: str = None, sep: str = None) -> None:
    with mmap(fileno, 0, access=ACCESS_READ) as mm:
        print_ordered_strings(min_length, mm, radix, sep)

def replace_all_string(binary: bytes, starts: list, replacement: bytes) -> None:
    for i, c in enumerate(replacement):
        for start in starts:
            binary[start + i] = c
def replace_all_file(starts: dict, replacement: bytes, fileno: int) -> None:
    with mmap(fileno, 0, access=ACCESS_WRITE) as mm:
        replace_all_string(mm, starts, replacement)

def int_gt_one(value: str) -> int:
    try:
        ivalue = int(value)
    except ValueError:
        raise ArgumentTypeError(f"{value} is not an integer")
    if ivalue <= 1:
        raise ArgumentTypeError("minimal byte count must be > 1")
    return ivalue

def radix_type(value: str) -> str:
    if value not in "odx" and value is not None:
        raise ArgumentTypeError("radix must be either o, d or x")
    return value

def method_type(value: str) -> str:
    if value not in "lrL":
        raise ArgumentTypeError("method must be either l, r or L")
    return value

class MaxLengthValidator(Validator):
    def __init__(self, max_len):
        super().__init__()
        self.max_len = max_len
    def validate(self, document):
        if len(document.text) > self.max_len:
            raise ValidationError(
                message="Replacement cannot be longer than original string",
                cursor_position=len(document.text)
            )
def sanitize(replacement: str, to_size: int, method: str = "L") -> str:
    if method == 'l': return replacement.rjust(to_size)
    if method == 'r': return replacement.ljust(to_size)
    return replacement
