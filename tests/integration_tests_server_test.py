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
