from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.client.get("/")

    @task
    def showsummary(self):
        self.client.post("/showSummary", {"email": "john@simplylift.co"})

    @task
    def book(self):
        self.client.get("/book/Spring Festival/Simply Lift")

    @task
    def purchasesPlaces(self):
        self.client.post(
            "/purchasePlaces",
            {"club": "Simply Lift", "competition": "Fall Classic", "places": "6"},
        )

    @task
    def totalClubPoints(self):
        self.client.get("/totalClubPoints")

    def on_stop(self):
        self.client.get("/logout")
