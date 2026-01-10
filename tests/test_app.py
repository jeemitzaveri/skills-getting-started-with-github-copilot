from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_get_activities():
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister():
    email = "test.student@example.com"
    activity = "Basketball Team"

    # Ensure email not present initially
    r = client.get("/activities")
    assert email not in r.json()[activity]["participants"]

    # Sign up
    r = client.post(f"/activities/{activity}/signup?email={email}")
    assert r.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]

    # Duplicate signup returns 400
    r = client.post(f"/activities/{activity}/signup?email={email}")
    assert r.status_code == 400

    # Unregister
    r = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert r.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]
