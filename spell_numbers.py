"""Convert numbers from digits to words in Basque (eus)."""


from argparse import ArgumentParser
import sys


LANGUAGES = [
    # uncomment "est" below if you implement Estonian numbers,
    # or "eus" if you implement Basque numbers
    
    # "est",
     "eus",
]


def eus(n):
    """Spell an integer in Standard Basque (0–999,999).

    Args:
        n (int): Integer to spell. Must be in the range 0–999999 inclusive.

    Returns:
        str: The number written in Basque with single spaces between words.

    Raises:
        ValueError: If n is outside the allowed range.
    """
    if not (0 <= n <= 999_999):
        raise ValueError("n must be between 0 and 999999")

    # 0–9
    ONES = [
        "zero", "bat", "bi", "hiru", "lau", "bost", "sei", "zazpi", "zortzi", "bederatzi"
    ]

    # 10–19 (fixed forms)
    TEENS = {
        10: "hamar",
        11: "hamaika",
        12: "hamabi",
        13: "hamairu",
        14: "hamalau",
        15: "hamabost",
        16: "hamasei",
        17: "hamazazpi",
        18: "hamazortzi",
        19: "hemeretzi",
    }

    # 20/40/60/80 bases
    TWENTY_BASES = {
        20: "hogei",
        40: "berrogei",
        60: "hirurogei",
        80: "laurogei",
    }

    # 100s (exact multiples)
    HUNDREDS = {
        100: "ehun",
        200: "berrehun",
        300: "hirurehun",
        400: "laurehun",
        500: "bostehun",
        600: "seiehun",
        700: "zazpiehun",
        800: "zortziehun",
        900: "bederatziehun",
    }

    def words_under_100(m: int) -> str:
        # 0–9
        if m < 10:
            return ONES[m]
        # 10–19
        if m < 20:
            return TEENS[m]
        # 20/40/60/80 exactly
        if m in TWENTY_BASES:
            return TWENTY_BASES[m]
        # For other values >=20:
        # Determine the nearest lower multiple of 20
        base = (m // 20) * 20
        tail = m - base
        # Base connector uses "-ta" form (e.g., "hogeita", "berrogeita", ...)
        base_word = TWENTY_BASES[base] + "ta"
        # Tail can be 10–19 ("hamar"/teens) or 1–9 (ones)
        if tail in TEENS:
            return f"{base_word} {TEENS[tail]}"
        else:
            return f"{base_word} {ONES[tail]}"

    def words_under_1000(m: int) -> str:
        if m < 100:
            return words_under_100(m)
        # exact multiples of 100
        if m in HUNDREDS:
            return HUNDREDS[m]
        h = (m // 100) * 100
        r = m - h
        return f"{HUNDREDS[h]} eta {words_under_100(r)}"

    # 0–999
    if n < 1000:
        return words_under_1000(n)

    # 1,000–999,999
    thousands = n // 1000
    rest = n % 1000

    if thousands == 1:
        thou_words = "mila"
    else:
        thou_words = f"{words_under_1000(thousands)} mila"

    if rest == 0:
        return thou_words
    # Use "eta" between thousands and rest only when rest < 100
    if rest < 100:
        return f"{thou_words} eta {words_under_100(rest)}"
    else:
        return f"{thou_words} {words_under_1000(rest)}"


def main(lang, input_file, output_file):
    """Read numbers from a file and write "<number> = <words>" lines to output.

    Args:
        lang (str): ISO 639-3 language code; only "eus" is accepted here.
        input_file (str): Path to UTF-8 file containing one integer per line.
        output_file (str): Path to UTF-8 file to create/overwrite.

    Side effects:
        Creates or overwrites the output file with converted lines.

    Raises:
        ValueError: If the language code is unsupported.
    """
    if lang not in LANGUAGES:
        raise ValueError("Unsupported language code")

    with open(input_file, "r", encoding="utf-8") as fin,          open(output_file, "w", encoding="utf-8") as fout:
        for line in fin:
            s = line.strip()
            if not s:
                continue
            n = int(s)
            if lang == "eus":
                spelled = eus(n)
            else:
                # Placeholder for "est" if ever enabled
                raise ValueError("Only Basque (eus) implemented in this solution.")
            fout.write(f"{n} = {spelled}\n")


def parse_args(arglist):
    """Parse command-line arguments.

    Args:
        arglist (list[str]): Arguments (excluding program name).

    Returns:
        namespace: the parsed arguments as a namespace. The following attributes
        will be defined: lang, input_file, and output_file. See above for
        details.
    """
    parser = ArgumentParser()
    parser.add_argument("lang", help="ISO 639-3 language code")
    parser.add_argument("input_file", help="input file containing numbers")
    parser.add_argument("output_file", help="file where output will be stored")
    return parser.parse_args(arglist)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.lang, args.input_file, args.output_file)