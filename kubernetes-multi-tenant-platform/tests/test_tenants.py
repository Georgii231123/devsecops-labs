from scripts.render_tenants import load_tenants, render_tenant


def test_tenant_names_are_unique():
    tenants = load_tenants(__import__("pathlib").Path("config/tenants.yaml"))
    names = [tenant["name"] for tenant in tenants]
    assert len(names) == len(set(names))


def test_every_tenant_gets_default_deny_and_restricted_psa():
    tenants = load_tenants(__import__("pathlib").Path("config/tenants.yaml"))
    for tenant in tenants:
        docs = render_tenant(tenant)
        namespace = next(doc for doc in docs if doc["kind"] == "Namespace")
        assert namespace["metadata"]["labels"]["pod-security.kubernetes.io/enforce"] == "restricted"
        policies = {doc["metadata"]["name"] for doc in docs if doc["kind"] == "NetworkPolicy"}
        assert "default-deny" in policies


def test_tenant_role_has_no_secret_or_wildcard_access():
    tenants = load_tenants(__import__("pathlib").Path("config/tenants.yaml"))
    for tenant in tenants:
        role = next(doc for doc in render_tenant(tenant) if doc["kind"] == "Role")
        for rule in role["rules"]:
            assert "secrets" not in rule["resources"]
            assert "*" not in rule["resources"]
            assert "*" not in rule["verbs"]
