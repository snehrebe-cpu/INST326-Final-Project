from argparse import ArgumentParser
import re
import sys


LETTER_TO_NUMBER = {
    'A': '2',
    'B': '2',
    'C': '2',
    'D': '3',
    'E': '3',
    'F': '3',
    'G': '4',
    'H': '4',
    'I': '4',
    'J': '5',
    'K': '5',
    'L': '5',
    'M': '6',
    'N': '6',
    'O': '6',
    'P': '7',
    'Q': '7',
    'R': '7',
    'S': '7',
    'T': '8',
    'U': '8',
    'V': '8',
    'W': '9',
    'X': '9',
    'Y': '9',
    'Z': '9'
}


class PhoneNumber:
    """Represent a NANP phone number with comparison and formatting."""

def __init__(self, raw):
    """Initialize from a string or integer.

    Args:
        raw: phone number as str or int.

    Raises:
        TypeError: if raw is not str or int.
        ValueError: if number is not a valid NANP number.
    """
    if not isinstance(raw, (str, int)):
        raise TypeError("PhoneNumber expects a string or integer")

    if isinstance(raw, int):
        raw_str = str(raw)
    else:
        raw_str = str(raw)

    # Replace letters with digits using LETTER_TO_NUMBER
    def letter_to_digit(match):
        ch = match.group(0).upper()
        return LETTER_TO_NUMBER[ch]

    # First turn letters into digits
    raw_str = re.sub(r"[A-Za-z]", letter_to_digit, raw_str)

    # Remove everything except digits
    digits = re.sub(r"[^0-9]", "", raw_str)

    # Handle optional leading 1 for country code
    if len(digits) == 11 and digits[0] == "1":
        digits = digits[1:]
    elif len(digits) == 11:
        raise ValueError("Invalid country code")
    elif len(digits) != 10:
        raise ValueError("Phone number must have 10 digits after cleaning")

    area = digits[0:3]
    exchange = digits[3:6]
    line = digits[6:10]

    # NANP rules
    # Area code and exchange code must not start with 0 or 1
    if area[0] in ("0", "1") or exchange[0] in ("0", "1"):
        raise ValueError("Area and exchange codes must not start with 0 or 1")

    # Area code and exchange code must not end with 11
    if area.endswith("11") or exchange.endswith("11"):
        raise ValueError("Area and exchange codes must not end with 11")

    self.area_code = area
    self.exchange_code = exchange
    self.line_number = line
    self._digits = digits

def __int__(self):
    """Return the number as an int."""
    return int(self._digits)

def __repr__(self):
    """Return an unambiguous representation."""
    return f"PhoneNumber('{self._digits}')"

def __str__(self):
    """Return standard formatted string."""
    return f"({self.area_code}) {self.exchange_code}-{self.line_number}"

def __lt__(self, other):
    """Compare numbers by their digits."""
    if not isinstance(other, PhoneNumber):
        return NotImplemented
    return self._digits < other._digits

def __eq__(self, other):
    """Check equality by digits."""
    if not isinstance(other, PhoneNumber):
        return NotImplemented
    return self._digits == other._digits


def read_numbers(path):
    """Read valid phone numbers from a file and return sorted results.
    Args:
        path (str): path to a UTF-8 text file with name, tab, number.
    Returns:
        list of (name, PhoneNumber) tuples sorted by phone number.
    """
    results = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            parts = line.split("\t", 1)
            if len(parts) != 2:
                continue
            name, num_str = parts[0], parts[1]
            try:
                number = PhoneNumber(num_str)
            except (TypeError, ValueError):
                # Skip invalid numbers
                continue
            results.append((name, number))
    results.sort(key=lambda pair: pair[1])
    return results


def main(path):
    """Read data from path and print results.
    
    Args:
        path (str): path to a text file. Each line in the file should consist of
            a name, a tab character, and a phone number.
    
    Side effects:
        Writes to stdout.
    """
    for name, number in read_numbers(path):
        print(f"{number}\t{name}")

def parse_args(arglist):
    """Parse command-line arguments.
    
    Expects one mandatory command-line argument: a path to a text file where
    each line consists of a name, a tab character, and a phone number.
    
    Args:
        arglist (list of str): a list of command-line arguments to parse.
        
    Returns:
        argparse.Namespace: a namespace object with a file attribute whose value
        is a path to a text file as described above.
    """
    parser = ArgumentParser()
    parser.add_argument("file", help="file of names and numbers")
    return parser.parse_args(arglist)

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.file)