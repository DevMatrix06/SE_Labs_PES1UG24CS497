import math

from hypothesis import given, strategies as st
from processor import (
    verify_isbn10_format,
    calculate_depreciation_factor,
    lookup_condition_multiplier,
)


# ---------------------------------------------------------------------------
# Part 1: "does it crash?" tests (the ones the handout asks for).
# Each function gets random text or None and must never raise.
# ---------------------------------------------------------------------------

@given(st.text() | st.none())
def test_verify_isbn10_format_no_crash(s):
    try:
        verify_isbn10_format(s)
    except Exception as e:
        assert False, f"verify_isbn10_format crashed with: {e!r} on input {s!r}"


@given(st.text() | st.none())
def test_calculate_depreciation_factor_safe(s):
    try:
        calculate_depreciation_factor(s)
    except Exception as e:
        assert False, f"calculate_depreciation_factor crashed with: {e!r} on input {s!r}"


@given(st.text() | st.none())
def test_lookup_condition_multiplier_safe(s):
    try:
        lookup_condition_multiplier(s)
    except Exception as e:
        assert False, f"lookup_condition_multiplier crashed with: {e!r} on input {s!r}"


# ---------------------------------------------------------------------------
# Part 2: a few extra checks. Random text rarely looks like a real ISBN or
# a real "3/10", so these generate structured input to reach the happy path.
# ---------------------------------------------------------------------------

# Wrong types (ints, floats, lists...) should be handled too, not just str/None.
@given(st.one_of(st.integers(), st.floats(), st.binary(), st.lists(st.integers())))
def test_non_string_input_does_not_crash(x):
    verify_isbn10_format(x)
    calculate_depreciation_factor(x)
    lookup_condition_multiplier(x)


@given(st.from_regex(r"[0-9]-[0-9]{3}-[0-9]{5}-[0-9X]", fullmatch=True))
def test_well_formed_isbn_is_accepted(isbn):
    result = verify_isbn10_format(isbn)
    assert result is not None
    assert result.startswith("Group ")


@given(
    st.floats(min_value=0, max_value=1000, allow_nan=False),
    st.floats(min_value=0.001, max_value=1000, allow_nan=False),
)
def test_depreciation_factor_stays_in_range(age, life):
    factor = calculate_depreciation_factor(f"{age}/{life}")
    assert factor is not None
    assert 0.1 <= factor <= 1.0


def test_depreciation_rejects_nan_and_inf():
    for bad in ("nan", "inf", "-inf"):
        result = calculate_depreciation_factor(f"{bad}/10")
        assert result is None or math.isfinite(result)
        result = calculate_depreciation_factor(f"3/{bad}")
        assert result is None or math.isfinite(result)


@given(st.sampled_from(["MINT", "LIKE_NEW", "VERY_GOOD", "GOOD", "POOR"]),
       st.sampled_from(["", " ", "  "]))
def test_known_conditions_are_found_regardless_of_case_and_spaces(grade, pad):
    assert lookup_condition_multiplier(pad + grade.lower() + pad) is not None


def test_division_by_zero_lifespan():
    assert calculate_depreciation_factor("3/0") is None
