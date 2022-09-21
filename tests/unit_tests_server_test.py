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


class TestServer:
    def test_unknown_email(self, client):
        data = {"email": "unknown_email@gmail.com"}
        response = client.post(
            "/showSummary",
            data=data,
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert response.data.decode().find("Sorry, that email was not found.") != -1

    def test_known_email(self, client):
        data = {"email": "john@simplylift.co"}
        response = client.post(
            "/showSummary",
            data=data,
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert response.data.decode().find("Welcome, john@simplylift.co") != -1

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

    def test_points_club_points_competition_updated(self, client):
        data = {"club": "Simply Lift", "competition": "Spring Festival", "places": "4"}

        response = client.post(
            "/purchasePlaces",
            data=data,
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert response.data.decode().find("Points available: 1") != -1
        assert response.data.decode().find("Number of Places: 21") != -1

    def test_loadClubs(self):
        expected = [
            {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
            {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
            {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
        ]

        assert server.loadClubs("tests/clubs_test.json") == expected

    def test_loadCompetitions(self):
        expected = [
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

        assert server.loadCompetitions("tests/competitions_test.json") == expected

    def test_index(self, client):
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

    def test_book_valid_club_valid_competition(self, client):
        club = r"/Simply Lift"
        competition = r"Spring Festival"
        response = client.get(
            "/book/" + competition + club,
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert response.data.decode().find(competition) != -1
        assert response.data.decode().find("How many places?") != -1

    def test_book_no_valid_club_valid_competition(self, client):
        club = r"/imply Lift"
        competition = r"Spring Festival"
        response = client.get(
            "/book/" + competition + club,
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert (
            response.data.decode().find("competition or/and club are not valid") != -1
        )

    def test_logout(self, client):
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

    def test_totalClubPoints(self, client):
        response = client.get(
            "/totalClubPoints",
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert ("Points Display Board") != -1
        assert ("Simply Lift, 5 point(s)") != -1
        assert ("Iron Temple, 4 point(s)") != -1
        assert ("She Lifts, 12 point(s)") != -1
