from scripts.validate_portal import normalize_ref, validate


def test_portal_contract_is_valid() -> None:
    assert validate() == []


def test_reference_normalization() -> None:
    assert normalize_ref("payments", "system") == "system:default/payments"
    assert normalize_ref("group:payments") == "group:default/payments"
    assert normalize_ref("resource:default/payments-db") == "resource:default/payments-db"
