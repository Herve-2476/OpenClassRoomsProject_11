import pytest
from server import create_app
import server


@pytest.fixture
def client(mocker):
    def mock_loadClubs():
        listOfClubs = [
            {"name": "Simply Lift", "email": "ohn@simplylift.co", "points": "13"},
            {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
            {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
        ]
        return listOfClubs

    def mock_loadCompetitions():
        listOfCompetitions = [
            {
                "name": "Spring Festival",
                "date": "2020-03-27 10:00:00",
                "numberOfPlaces": "25",
            },
            {
                "name": "Fall Classic",
                "date": "2020-10-22 13:30:00",
                "numberOfPlaces": "13",
            },
        ]
        return listOfCompetitions

    mocker.patch("server.loadClubs", mock_loadClubs)
    mocker.patch("server.loadCompetitions", mock_loadCompetitions)
    mocker.patch.object(server, "POINT_INSCRIPTION_VALUE", 1)
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


class TestServer:
    # def __init__(self,clubs)
    def test_unknown_valid_email(self, client):
        data = {"email": "unknown_email@gmail.com"}
        response = client.post(
            "/showSummary",
            data=data,
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert (
            response.data.decode().find(
                "<h1>Welcome to the GUDLFT Registration Portal!</h1>"
            )
            != -1
        )

    def test_not_exceed_points_allowed(self, client):
        data = {"club": "Simply Lift", "competition": "Fall Classic", "places": "14"}

        response = client.post(
            "/purchasePlaces",
            data=data,
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert (
            response.data.decode().find("You do not have enough points to book") != -1
        )
