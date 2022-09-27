import pytest
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
    app = server.create_app({"TESTING": True})
    with app.test_client() as client:
        yield client
