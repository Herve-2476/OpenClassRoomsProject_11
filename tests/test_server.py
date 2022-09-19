import pytest
from server import create_app
import server


@pytest.fixture
def client(mocker):
    def mock_loadClubs():
        listOfClubs = [
            {"name": "Simply Lift", "email": "john@simplylift.co", "points": "5"},
            {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
            {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
        ]
        return listOfClubs

    def mock_loadCompetitions():
        listOfCompetitions = [
            {
                "name": "Spring Festival",
                "date": "2023-03-27 10:00:00",
                "numberOfPlaces": "25",
            },
            {
                "name": "Fall Classic",
                "date": "2020-10-22 13:30:00",
                "numberOfPlaces": "5",
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
        data = {"club": "Simply Lift", "competition": "Spring Festival", "places": "6"}

        response = client.post(
            "/purchasePlaces",
            data=data,
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert (
            response.data.decode().find("You do not have enough points to book") != -1
        )

    def test_not_book_more_12_places(self, client):
        data = {"club": "Simply Lift", "competition": "Spring Festival", "places": "13"}

        response = client.post(
            "/purchasePlaces",
            data=data,
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert response.data.decode().find("You cannot book more than 12 places") != -1

    def test_not_book_past_competition(self, client):
        data = {"club": "Simply Lift", "competition": "Fall Classic", "places": "4"}

        response = client.post(
            "/purchasePlaces",
            data=data,
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert response.data.decode().find("You cannot book in past competitions") != -1
