import src.app as app_module


def test_get_activities_returns_activity_catalog(client):
    # Arrange
    expected_activity_names = {"Chess Club", "Programming Class", "Gym Class", "Basketball Team", "Tennis Club", "Art Studio", "Music Band", "Debate Team", "Science Club"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert set(payload.keys()) == expected_activity_names
    assert payload["Chess Club"]["max_participants"] == 12
    assert payload["Chess Club"]["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_for_activity_rejects_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_unregister_from_activity_removes_participant(client):
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_from_activity_rejects_missing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "missing@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Student is not signed up for this activity"}


def test_unknown_activity_rejects_signup_and_unregister(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    signup_response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    unregister_response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert
    assert signup_response.status_code == 404
    assert signup_response.json() == {"detail": "Activity not found"}
    assert unregister_response.status_code == 404
    assert unregister_response.json() == {"detail": "Activity not found"}