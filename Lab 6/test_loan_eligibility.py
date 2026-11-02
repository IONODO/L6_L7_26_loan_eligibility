import pytest
from loan_eligibility import credit_band, is_eligible, interest_rate


def test_credit_band_valid_ranges():
    assert credit_band(300) == "poor"
    assert credit_band(550) == "fair"
    assert credit_band(650) == "good"
    assert credit_band(750) == "excellent"


def test_is_eligible_true_cases():
    assert is_eligible(30, 50000, "salaried", 800) is True
    assert is_eligible(45, 60000, "self_employed", 700) is True


def test_interest_rate_core_values():
    assert interest_rate(800, "salaried", False) == 8
    assert interest_rate(700, "salaried", False) == 10
    assert interest_rate(600, "salaried", False) == 13
    assert interest_rate(800, "self_employed", True) == 7