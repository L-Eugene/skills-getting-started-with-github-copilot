import pytest


@pytest.mark.parametrize(
    "activity_name,email",
    [
        ("Chess Club", "new.student@mergington.edu"),
        ("Programming Class", "edge+case@mergington.edu"),
        ("Gym Class", "not-an-email"),
    ],
)
def test_signup_success_and_participant_added(client, isolated_activities, activity_name, email):
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in isolated_activities[activity_name]["participants"]


def test_signup_duplicate_student_returns_400(client, isolated_activities):
    activity_name = "Chess Club"
    existing_email = isolated_activities[activity_name]["participants"][0]

    response = client.post(f"/activities/{activity_name}/signup", params={"email": existing_email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_unknown_activity_returns_404(client, isolated_activities):
    response = client.post("/activities/Unknown Club/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_activity_name_is_case_sensitive(client, isolated_activities):
    response = client.post("/activities/chess club/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
