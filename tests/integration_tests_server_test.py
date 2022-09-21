import pytest
from server import create_app
import server


@pytest.fixture
def client(mocker):
    def mock_loadClubs(json_file):
        listOfClubs = [
            {"name": "Simply Lift", "email": "john@simplylift.co", "points": "5"},
            {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
            {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
        ]
        return listOfClubs

    def mock_loadCompetitions(json_file):
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


def test_path(client):

    """
    test successively the following funtions

    - loadClubs
    - loadCompetitions
    - index
    - showSummary
    - book
    - purchasePlaces
    - logout

    """
    club = {"name": "Simply Lift", "email": "john@simplylift.co", "points": "5"}
    competition = {
        "name": "Spring Festival",
        "date": "2023-03-27 10:00:00",
        "numberOfPlaces": "25",
    }

    # index
    response = client.get(
        "/",
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert (
        response.data.decode().find(
            "<h1>Welcome to the GUDLFT Registration Portal!</h1>"
        )
        != -1
    )

    # showSummary

    response = client.post(
        "/showSummary",
        data=club,
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert response.data.decode().find("Welcome, john@simplylift.co") != -1

    # book

    response = client.get(
        "/".join(["/book", competition["name"], club["name"]]),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert response.data.decode().find(competition["name"]) != -1
    assert response.data.decode().find("How many places?") != -1

    # purchasePlaces
    data = {"club": club["name"], "competition": competition["name"], "places": "4"}

    response = client.post(
        "/purchasePlaces",
        data=data,
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert response.data.decode().find("Points available: 1") != -1
    assert response.data.decode().find("Number of Places: 21") != -1

    # logout
    response = client.get(
        "/logout",
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert (
        response.data.decode().find(
            "<h1>Welcome to the GUDLFT Registration Portal!</h1>"
        )
        != -1
    )
