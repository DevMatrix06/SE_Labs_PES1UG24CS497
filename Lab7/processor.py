import math
import re

# 9 digits followed by a digit or X (the ISBN-10 check character).
# [0-9] on purpose: \d would also match things like Arabic-Indic digits,
# which int() accepts but which are not valid in an ISBN.
_ISBN10_RE = re.compile(r"[0-9]{9}[0-9Xx]")

MULTIPLIERS = {
    "MINT": 1.25,
    "LIKE_NEW": 1.00,
    "VERY_GOOD": 0.80,
    "GOOD": 0.60,
    "POOR": 0.30,
}


def verify_isbn10_format(isbn_str):
    """Return a summary string for a well-formed ISBN-10, or None if it isn't one."""
    if not isinstance(isbn_str, str):
        return None

    # Hyphens and surrounding whitespace are allowed; anything else is not.
    cleaned = isbn_str.replace("-", "").strip()
    if not _ISBN10_RE.fullmatch(cleaned):
        return None

    first_digit = int(cleaned[0])
    group_code = cleaned[1:4]
    check_char = cleaned[9].upper()
    return f"Group {group_code}: Starts {first_digit}, Checksum {check_char}"


def calculate_depreciation_factor(book_age_str):
    """Parse 'age/lifespan' and return a factor between 0.1 and 1.0.

    Returns None when the input can't be parsed or makes no sense
    (missing slash, non-numbers, zero or negative lifespan, negative age,
    nan/inf).
    """
    if not isinstance(book_age_str, str):
        return None

    parts = book_age_str.split("/")
    if len(parts) != 2:
        return None

    try:
        age = float(parts[0])
        life = float(parts[1])
    except ValueError:
        return None

    if not (math.isfinite(age) and math.isfinite(life)):
        return None
    if age < 0 or life <= 0:
        return None

    depreciation = 1.0 - (age / life)
    # age/life can still overflow to inf for absurd values like 1e308/1e-308;
    # clamping keeps the result sane either way.
    if not math.isfinite(depreciation):
        return None
    return round(max(0.1, depreciation), 2)


def lookup_condition_multiplier(condition_code):
    """Return the price multiplier for a condition grade, or None if unknown."""
    if not isinstance(condition_code, str):
        return None

    # Be forgiving about "like new" / "Like-New" / " good ".
    grade = re.sub(r"[\s-]+", "_", condition_code.strip().upper())
    return MULTIPLIERS.get(grade)


def main():
    print("==== Running verify_isbn10_format ====")
    isbn_in = input("Enter ISBN-10 (e.g. 0-306-40615-2): ")
    isbn_out = verify_isbn10_format(isbn_in)
    print(isbn_out if isbn_out is not None else "Invalid ISBN-10 format.")

    print("\n==== Running calculate_depreciation_factor ====")
    age_in = input("Enter age/lifespan in years (e.g. 3/10): ")
    factor = calculate_depreciation_factor(age_in)
    if factor is None:
        print("Invalid input. Use the form age/lifespan with a positive lifespan, e.g. 3/10.")
    else:
        print("Depreciation Factor:", factor)

    print("\n==== Running lookup_condition_multiplier ====")
    cond_in = input("Enter condition (e.g. MINT, GOOD, POOR): ")
    mult = lookup_condition_multiplier(cond_in)
    if mult is None:
        print("Unknown condition. Choose from: " + ", ".join(MULTIPLIERS))
    else:
        print("Multiplier:", mult)


if __name__ == "__main__":
    main()
