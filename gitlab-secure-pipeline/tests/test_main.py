from app.main import sha256_text


def test_sha256_text_is_deterministic() -> None:
    assert sha256_text("devsecops") == (
        "da0a67a1d01482326c00ceb65117d8d56b031030bdcaf7e098b923b658b23fc2"
    )


def test_sha256_changes_with_input() -> None:
    assert sha256_text("devsecops") != sha256_text("DevSecOps")


def test_sha256_has_expected_length() -> None:
    assert len(sha256_text("security")) == 64
