import math
import pytest
from hypothesis import given, strategies as st

from loan_eligibility import parse_income, monthly_emi, pan_category, CATEGORIES


def test_parse_income_valid_examples():
    assert parse_income("50,000") == 50000
    assert parse_income(" 1 2 3 ") == 123
    assert parse_income(25000) == 25000
    assert parse_income(25000.9) == 25000


def test_monthly_emi_valid_example():
    assert monthly_emi("500000,10,5") == 10623.52


def test_pan_category_valid_examples():
    assert pan_category("ABCPE1234F") == "Individual"
    assert pan_category("ABCHX1234F") == "HUF"


@given(
    st.one_of(
        st.none(),
        st.text(),
        st.integers(),
        st.floats(allow_nan=True, allow_infinity=True),
        st.booleans(),
        st.lists(st.integers()),
        st.dictionaries(st.text(), st.integers()),
    )
)
def test_parse_income_fuzz_no_unexpected_exceptions(x):
    try:
        out = parse_income(x)
        assert isinstance(out, int)
        assert out >= 0
    except (ValueError, TypeError):
        pass


@given(
    st.one_of(
        st.none(),
        st.text(),
        st.tuples(
            st.one_of(st.text(), st.integers(), st.floats(allow_nan=False, allow_infinity=False)),
            st.one_of(st.text(), st.integers(), st.floats(allow_nan=False, allow_infinity=False)),
            st.one_of(st.text(), st.integers(), st.floats(allow_nan=False, allow_infinity=False)),
        ),
        st.lists(st.text(), min_size=0, max_size=6),
        st.integers(),
        st.floats(allow_nan=True, allow_infinity=True),
        st.booleans(),
    )
)
def test_monthly_emi_fuzz_no_unexpected_exceptions(x):
    try:
        out = monthly_emi(x)
        assert isinstance(out, float)
        assert math.isfinite(out)
        assert out >= 0
    except (ValueError, TypeError):
        pass


@given(
    st.one_of(
        st.none(),
        st.text(),
        st.integers(),
        st.floats(allow_nan=True, allow_infinity=True),
        st.booleans(),
        st.lists(st.text()),
    )
)
def test_pan_category_fuzz_no_unexpected_exceptions(x):
    try:
        out = pan_category(x)
        assert out in set(CATEGORIES.values())
    except (ValueError, TypeError):
        pass


@pytest.mark.parametrize(
    "bad_income",
    ["", " ", "-1", "12.34", "abc", object(), None, True],
)
def test_parse_income_rejects_invalid_inputs(bad_income):
    with pytest.raises((ValueError, TypeError)):
        parse_income(bad_income)


@pytest.mark.parametrize(
    "bad_details",
    [
        "",
        "1,2",
        "1,2,3,4",
        "a,b,c",
        "0,10,5",
        "1000,-1,1",
        "1000,10,0",
        None,
        True,
        object(),
    ],
)
def test_monthly_emi_rejects_invalid_inputs(bad_details):
    with pytest.raises((ValueError, TypeError)):
        monthly_emi(bad_details)


@pytest.mark.parametrize(
    "bad_pan",
    ["", "AB", "ABCD", "AAAAX1234Z", None, 123, True],
)
def test_pan_category_rejects_invalid_inputs(bad_pan):
    with pytest.raises((ValueError, TypeError)):
        pan_category(bad_pan)