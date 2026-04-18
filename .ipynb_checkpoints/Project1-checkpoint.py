"""
spell_numbers.py
Spells out numbers in Basque (eus).
"""

import argparse
import sys

# Uncomment correct language
LANGUAGES = [
    # "est",
    "eus",
]

# Basque words
ONES = ["zero", "bat", "bi", "hiru", "lau", "bost", "sei", "zazpi", "zortzi", "bederatzi"]
TENS = ["", "hamar", "hogei", "hogeita hamar", "berrogei", "berrogeita hamar",
        "hirurogei", "hirurogeita hamar", "laurogei", "laurogeita hamar"]
HUNDREDS = ["", "ehun", "berrehun", "hirurehun", "laurehun",
            "bostehun", "seiehunda", "zazpiehun", "zortziehun", "bederatziehun"]

def eus(n):
    """
    Convert an integer to Basque words.

    Args:
        n (int): Integer 0–999999.

    Returns:
        str: Number spelled in Basque.

    Raises:
        ValueError: If n is outside 0–999999.
    """
    if n < 0 or n > 999999:
        raise ValueError("Number out of range")

    if n < 10:
        return ONES[n]
    if n < 20:
        return "hamar" if n == 10 else "hamar" + " eta " + ONES[n - 10]
    if n < 100:
        tens, ones = divmod(n, 10)
        if ones == 0:
            return TENS[tens]
        return TENS[tens] + " eta " + ONES[ones]
    if n < 1000:
        hundreds, rest = divmod(n, 100)
        if rest == 0:
            return HUNDREDS[hundreds]
        return HUNDREDS[hundreds] + " eta " + eus(rest)
    if n < 1000000:
        thousands, rest = divmod(n, 1000)
        prefix = "mila" if thousands == 1 else eus(thousands) + " mila"
        if rest == 0:
            return prefix
        return prefix + " eta " + eus(rest)

    raise ValueError("Unhandled case")


def main(lang, infile, outfile):
    """
    Read numbers from infile and write words to outfile.

    Args:
        lang (str): "eus" (Basque).
        infile (str): Path to input file.
        outfile (str): Path to output file.

    Side effects:
        Creates/overwrites outfile with results.

    Raises:
        ValueError: If lang is not supported.
    """
    if lang not in LANGUAGES:
        raise ValueError("Unsupported language code")

    with open(infile, "r", encoding="utf-8") as fin, \
         open(outfile, "w", encoding="utf-8") as fout:
        for line in fin:
            num = int(line.strip())
            word = eus(num)
            fout.write(f"{num} = {word}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("lang")
    parser.add_argument("infile")
    parser.add_argument("outfile")
    args = parser.parse_args()
    main(args.lang, args.infile, args.outfile)