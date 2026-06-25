import pytest


@pytest.mark.parametrize(
    "activity_name",
    ["Chess Club", "Programming Class", "Gym Class"],
)
def test_unregister_success_removes_participant(client, isolated_activities, activity_name):
    email = isolated_activities[activity_name]["participants"][0]

    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in isolated_activities[activity_name]["participants"]


def test_unregister_unknown_activity_returns_404(client, isolated_activities):
    response = client.delete(
        "/activities/Unknown Club/participants",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_missing_participant_returns_404(client, isolated_activities):
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": "missing@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_activity_state_is_restored_between_tests(client, isolated_activities):
    activity_name = "Chess Club"
    email = isolated_activities[activity_name]["participants"][0]

    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    assert response.status_code == 200
    assert email not in isolated_activities[activity_name]["participants"]
