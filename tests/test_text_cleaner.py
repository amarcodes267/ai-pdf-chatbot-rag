from services.text_cleaner import clean_text


def test_clean_text_basic():
    raw = "  This  is   a   test.\n\n\nNew paragraph.\t\tExtra spaces.  "
    cleaned = clean_text(raw)

    assert "  " not in cleaned
    assert "\t" not in cleaned
    assert cleaned.count("\n\n") == 1
    assert cleaned.startswith("This is a test")
