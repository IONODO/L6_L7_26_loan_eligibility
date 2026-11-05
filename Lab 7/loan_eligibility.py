from __future__ import annotations
import math

CATEGORIES = {
    "P": "Individual",
    "C": "Company",
    "H": "HUF",
    "F": "Firm",
}


def parse_income(income):
    if income is None:
        raise ValueError("Income cannot be None")
    if isinstance(income, bool):
        raise TypeError("Income cannot be a boolean")

    if isinstance(income, int):
        if income < 0:
            raise ValueError("Income cannot be negative")
        return income

    if isinstance(income, float):
        if not math.isfinite(income):
            raise ValueError("Income must be finite")
        if income < 0:
            raise ValueError("Income cannot be negative")
        return int(income)

    if not isinstance(income, str):
        raise TypeError("Income must be a string or number")

    cleaned = income.strip().replace(",", "").replace("_", "").replace(" ", "")
    if cleaned == "":
        raise ValueError("Income cannot be empty")

    if cleaned[0] == "+":
        cleaned = cleaned[1:]

    if not cleaned.isdigit():
        raise ValueError("Income must contain only digits (plus optional commas/spaces)")

    value = int(cleaned)
    if value < 0:
        raise ValueError("Income cannot be negative")
    return value


def monthly_emi(details):
    if details is None:
        raise ValueError("Details cannot be None")

    if isinstance(details, str):
        parts = [p.strip() for p in details.split(",")]
    elif isinstance(details, (list, tuple)) and len(details) == 3:
        parts = [str(x).strip() for x in details]
    else:
        raise TypeError("Details must be a comma-separated string or a 3-item sequence")

    if len(parts) != 3:
        raise ValueError("Details must have principal,rate,years")

    principal_s, rate_s, years_s = parts

    try:
        principal = float(principal_s)
        rate = float(rate_s)
        years = float(years_s)
    except Exception as exc:
        raise ValueError("Principal, rate, years must be numeric") from exc

    if not (math.isfinite(principal) and math.isfinite(rate) and math.isfinite(years)):
        raise ValueError("Principal, rate, years must be finite numbers")
    if principal <= 0:
        raise ValueError("Principal must be > 0")
    if rate < 0:
        raise ValueError("Rate cannot be negative")
    if years <= 0:
        raise ValueError("Years must be > 0")

    n_float = years * 12
    if n_float <= 0:
        raise ValueError("Total months must be > 0")
    n = int(n_float)
    if n == 0:
        raise ValueError("Total months cannot be 0")

    if rate == 0:
        emi = principal / n
        if not math.isfinite(emi):
            raise ValueError("Computed EMI is not finite")
        return round(emi, 2)

    r = rate / 1200.0
    base = 1.0 + r

    try:
        base_pow_n = base ** n
        denom = base_pow_n - 1.0
        if denom == 0:
            raise ValueError("Invalid EMI denominator")
        emi = principal * r * base_pow_n / denom
    except OverflowError as exc:
        raise ValueError("Input values are too large to compute EMI safely") from exc

    if not math.isfinite(emi):
        raise ValueError("Computed EMI is not finite")
    return round(emi, 2)

def pan_category(pan):
    if pan is None:
        raise ValueError("PAN cannot be None")
    if not isinstance(pan, str):
        raise TypeError("PAN must be a string")

    pan = pan.strip()
    if len(pan) < 4:
        raise ValueError("PAN is too short to determine category")

    key = pan[3].upper()
    if key not in CATEGORIES:
        raise ValueError("Unknown PAN category code")
    return CATEGORIES[key]


def main():
    print("==== Running parse_income ====")
    user_input = input("Enter monthly income (e.g. 50,000): ")
    try:
        result = parse_income(user_input)
        print("Income:", result)
    except Exception as e:
        print("Error:", e)

    print("\n==== Running monthly_emi ====")
    user_input = input("Enter principal,rate,years (e.g. 500000,10,5): ")
    try:
        result = monthly_emi(user_input)
        print("Monthly EMI:", result)
    except Exception as e:
        print("Error:", e)

    print("\n==== Running pan_category ====")
    user_input = input("Enter a PAN number (e.g. ABCPE1234F): ")
    try:
        result = pan_category(user_input)
        print("PAN Category:", result)
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()