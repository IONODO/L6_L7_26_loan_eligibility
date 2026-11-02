import pytest
from loan_eligibility import credit_band, is_eligible, interest_rate


def test_credit_band_excellent():
    assert credit_band(800) == "excellent"


def test_credit_band_good():
    assert credit_band(700) == "good"


def test_credit_band_fair():
    assert credit_band(600) == "fair"


def test_credit_band_poor():
    assert credit_band(300) == "poor"


def test_is_eligible_valid_salaried_application():
    assert is_eligible(30, 50000, "salaried", 800) is True


def test_is_eligible_valid_self_employed_application():
    assert is_eligible(45, 60000, "self_employed", 700) is True


def test_interest_rate_excellent_no_collateral():
    assert interest_rate(800, "salaried", False) == 8


def test_interest_rate_good_no_collateral():
    assert interest_rate(700, "salaried", False) == 10


def test_interest_rate_fair_no_collateral():
    assert interest_rate(600, "salaried", False) == 13


def test_interest_rate_self_employed_with_collateral():
    assert interest_rate(800, "self_employed", True) == 7