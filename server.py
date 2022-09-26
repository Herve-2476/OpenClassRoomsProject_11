import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime

POINT_INSCRIPTION_VALUE = 3


def loadClubs(json_file):
    with open(json_file) as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions(json_file):
    with open(json_file) as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


def create_app(conf):
    app = Flask(__name__)
    app.config["TESTING"] = conf.get("TESTING")
    app.secret_key = "something_special"

    competitions = loadCompetitions("competitions.json")
    clubs = loadClubs("clubs.json")

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/showSummary", methods=["POST"])
    def showSummary():
        try:
            club = [club for club in clubs if club["email"] == request.form["email"]][0]
            return render_template("welcome.html", club=club, competitions=competitions)
        except IndexError:
            flash("Sorry, that email was not found")
            return render_template("index.html")

    @app.route("/book/<competition>/<club>")
    def book(competition, club):
        try:
            foundClub = [c for c in clubs if c["name"] == club][0]
            foundCompetition = [c for c in competitions if c["name"] == competition][0]
        except IndexError:
            flash("competition or/and club are not valid")
            return redirect("/")

        if foundClub and foundCompetition:
            return render_template(
                "booking.html", club=foundClub, competition=foundCompetition
            )
        else:
            flash("Something went wrong-please try again")
            return render_template("welcome.html", club=club, competitions=competitions)

    @app.route("/purchasePlaces", methods=["POST"])
    def purchasePlaces():
        competition = [
            c for c in competitions if c["name"] == request.form["competition"]
        ][0]
        club = [c for c in clubs if c["name"] == request.form["club"]][0]
        placesRequired = int(request.form["places"])

        if datetime.now() > datetime.fromisoformat(competition["date"]):
            flash("You cannot book in past competitions")

        elif placesRequired > 12:
            flash("You cannot book more than 12 places")

        elif int(club["points"]) < placesRequired * POINT_INSCRIPTION_VALUE:
            flash(
                f"""You do not have enough points to book {placesRequired} places
                 ( {POINT_INSCRIPTION_VALUE} points per place )"""
            )
        else:
            competition["numberOfPlaces"] = (
                int(competition["numberOfPlaces"]) - placesRequired
            )
            club["points"] = (
                int(club["points"]) - placesRequired * POINT_INSCRIPTION_VALUE
            )

            flash("Great-booking complete!")
        return render_template("welcome.html", club=club, competitions=competitions)

    # TODO: Add route for points display
    @app.route("/totalClubPoints")
    def totalClubPoints():
        return render_template("totalClubPoints.html", clubs=clubs)

    @app.route("/logout")
    def logout():
        return redirect(url_for("index"))

    return app


app = create_app({"TESTING": False})
if __name__ == "__main__":

    app.run()
