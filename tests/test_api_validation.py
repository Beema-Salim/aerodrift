from dashboard import validate_api_data


def test_valid_topology_response():
    data = {
        "nodes": 8,
        "edges": 3
    }

    assert validate_api_data(data, ["nodes", "edges"])


def test_invalid_topology_response():
    data = {
        "nodes": "8",
        "edges": 3
    }

    assert not validate_api_data(data, ["nodes", "edges"])


def test_valid_drift_response():
    data = {
        "drift_count": 0,
        "issues": []
    }

    assert validate_api_data(data, ["drift_count", "issues"])


def test_valid_remediation_response():
    data = {
        "status": "pending",
        "actions": []
    }

    assert validate_api_data(data, ["status", "actions"])