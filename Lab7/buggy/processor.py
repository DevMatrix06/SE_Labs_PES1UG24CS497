def verify_isbn10_format(isbn_str):
    cleaned = isbn_str.replace('-', '').strip()
    first_digit = int(cleaned[0])
    group_code = cleaned[1:4]
    check_char = cleaned[9].upper()
    return f"Group {group_code}: Starts {first_digit}, Checksum {check_char}"

def calculate_depreciation_factor(book_age_str):
    age_str, life_str = book_age_str.split('/')
    age = float(age_str)
    life = float(life_str)
    depreciation = 1.0 - (age / life)
    return round(max(0.1, depreciation), 2)

def lookup_condition_multiplier(condition_code):
    grade = condition_code.strip().upper()
    multipliers = {
        "MINT": 1.25,
        "LIKE_NEW": 1.00,
        "VERY_GOOD": 0.80,
        "GOOD": 0.60,
        "POOR": 0.30
    }
    return multipliers[grade]

def main():
    print("==== Running verify_isbn10_format ====")
    isbn_in = input("Enter ISBN-10 (e.g. 0-306-40615-2): ")
    print(verify_isbn10_format(isbn_in))

    print("\n==== Running calculate_depreciation_factor ====")
    age_in = input("Enter age/lifespan in years (e.g. 3/10): ")
    print("Depreciation Factor:", calculate_depreciation_factor(age_in))

    print("\n==== Running lookup_condition_multiplier ====")
    cond_in = input("Enter condition (e.g. MINT, GOOD, POOR): ")
    print("Multiplier:", lookup_condition_multiplier(cond_in))

if __name__ == "__main__":
    main()