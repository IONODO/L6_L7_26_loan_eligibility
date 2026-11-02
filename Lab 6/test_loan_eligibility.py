import pytest
from loan_eligibility import credit_band, is_eligible, interest_rate

# credit_band tests
@pytest.mark.parametrize(
    "score, expected",
    [
        (300, "poor"),
        (549, "poor"),
        (550, "fair"),
        (649, "fair"),
        (650, "good"),
        (749, "good"),
        (750, "excellent"),
        (900, "excellent"),
    ],
)
def test_credit_band_valid_scores(score, expected):
    assert credit_band(score) == expected


@pytest.mark.parametrize("score", [299, 901])
def test_credit_band_invalid_scores(score):
    with pytest.raises(ValueError, match="invalid score"):
        credit_band(score)


# is_eligible tests
def test_is_eligible_valid_case():
    assert is_eligible(30, 50000, "salaried", 800) is True
    assert is_eligible(45, 50000, "self_employed", 750) is True


def test_is_eligible_invalid_employment():
    with pytest.raises(ValueError, match="unknown employment"):
        is_eligible(30, 50000, "contractor", 800)


@pytest.mark.parametrize(
    "age, income, employment, score",
    [
        (20, 50000, "salaried", 800),   # age too low
        (61, 50000, "salaried", 800),   # age too high
        (30, 24999, "salaried", 800),   # income too low
        (30, 50000, "salaried", 300),   # poor credit band
        (30, 35000, "self_employed", 800),  # income below self-employed minimum
    ],
)
def test_is_eligible_false_cases(age, income, employment, score):
    assert is_eligible(age, income, employment, score) is False


# interest_rate tests
@pytest.mark.parametrize(
    "score, employment, has_collateral, expected",
    [
        (800, "salaried", False, 8),      # excellent band
        (700, "self_employed", False, 11),  # good band + self-employed
        (600, "salaried", True, 11),      # fair band + collateral
        (800, "self_employed", True, 7),  # excellent band + self-employed + collateral
    ],
)
def test_interest_rate(score, employment, has_collateral, expected):
    assert interest_rate(score, employment, has_collateral) == expected