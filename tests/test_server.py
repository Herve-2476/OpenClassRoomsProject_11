import pytest
from server import create_app


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    print("ok", app)
    with app.test_client() as client:
        yield client


class TestServer:
    # def __init__(self,clubs)
    def test_unknown_valid_email(self, client):
        data = {"email": "unknown_email@gmail.com"}
        # data = {"email": "john@simplylift.co"}
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
