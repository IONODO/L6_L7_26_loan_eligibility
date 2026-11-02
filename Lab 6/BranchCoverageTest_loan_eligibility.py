import pytest
from loan_eligibility import credit_band, is_eligible, interest_rate


@pytest.mark.parametrize("score", [299, 901])
def test_credit_band_invalid_score(score):
    with pytest.raises(ValueError, match="invalid score"):
        credit_band(score)


def test_is_eligible_age_too_low():
    assert is_eligible(20, 50000, "salaried", 800) is False


def test_is_eligible_age_too_high():
    assert is_eligible(61, 50000, "salaried", 800) is False


def test_is_eligible_income_too_low():
    assert is_eligible(30, 24000, "salaried", 800) is False


def test_is_eligible_self_employed_income_too_low():
    assert is_eligible(30, 45000, "self_employed", 800) is False


def test_is_eligible_poor_credit_rejected():
    assert is_eligible(30, 50000, "salaried", 300) is False


def test_is_eligible_unknown_employment():
    with pytest.raises(ValueError, match="unknown employment"):
        is_eligible(30, 50000, "contractor", 800)


@pytest.mark.parametrize(
    "score, employment, has_collateral, expected",
    [
        (700, "self_employed", False, 11),
        (600, "salaried", True, 11),
        (800, "self_employed", True, 7),
    ],
)
def test_interest_rate_branch_variants(score, employment, has_collateral, expected):
    assert interest_rate(score, employment, has_collateral) == expected