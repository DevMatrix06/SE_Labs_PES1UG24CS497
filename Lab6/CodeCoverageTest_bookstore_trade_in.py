import pytest
from bookstore_trade_in import process_book_buybacks, inspect_scanner_calibration


def book(condition="good", missing=0, counterfeit=False):
    return {"missing_pages": missing, "condition": condition, "counterfeit": counterfeit}


def batch(fmt="paperback", books=None, approved=True, credit=False):
    return {
        "intake_approved": approved,
        "format": fmt,
        "payout_in_credit": credit,
        "books": books if books is not None else [book()],
    }


def test_single_paperback_good():
    result = process_book_buybacks([batch()], 5.0)
    assert result == {"total_payout": 8.0, "status": "COMPLETED"}


def test_invalid_batches_type():
    with pytest.raises(ValueError):
        process_book_buybacks("not a list", 5.0)


def test_unapproved_batch_skipped():
    result = process_book_buybacks([batch(approved=False)], 5.0)
    assert result == {"total_payout": 0.0, "status": "ZERO_CREDIT"}


def test_textbook_mint():
    result = process_book_buybacks([batch("textbook", [book("mint")])], 0)
    assert result["total_payout"] == 50.0


def test_hardcover_poor():
    result = process_book_buybacks([batch("hardcover", [book("poor")])], 0)
    assert result["total_payout"] == 6.0


def test_missing_pages_rejected():
    result = process_book_buybacks([batch(books=[book(missing=3)])], 0)
    assert result["status"] == "ZERO_CREDIT"


def test_counterfeit_textbook_zeroes_batch():
    books = [book(), book(counterfeit=True), book()]
    result = process_book_buybacks([batch("textbook", books)], 0)
    assert result["total_payout"] == 0.0


def test_credit_bonus_added():
    result = process_book_buybacks([batch(credit=True)], 5.0)
    assert result["total_payout"] == 13.0


def test_audit_rejected():
    books = [book(missing=1)] * 5
    result = process_book_buybacks([batch(books=books)], 0)
    assert result["status"] == "AUDIT_REJECTED"


def test_scanner_no_data():
    assert inspect_scanner_calibration([]) == "NO_DATA"


def test_scanner_recalibrate():
    assert inspect_scanner_calibration([[1, 6, 7]]) == "RECALIBRATE"
