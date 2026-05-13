import os

from flask import Flask, flash, redirect, render_template, request, url_for

from voting import cast_vote, get_results, parties


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-change-me")

    @app.get("/")
    def index():
        return render_template("index.html", parties=parties)

    @app.post("/vote")
    def vote():
        name = request.form.get("name", "")
        voter_id = request.form.get("voter_id", "")
        choice_raw = request.form.get("choice", "")

        try:
            choice = int(choice_raw)
        except ValueError:
            flash("Please select a party.", "error")
            return redirect(url_for("index"))

        try:
            party = cast_vote(name=name, voter_id=voter_id, choice=choice)
        except ValueError as e:
            flash(str(e), "error")
            return redirect(url_for("index"))

        return render_template("success.html", name=(name or "").strip() or "Voter", party=party)

    @app.get("/results")
    def results():
        # Optional simple guard (set RESULTS_PIN in env to enable)
        required_pin = os.environ.get("RESULTS_PIN")
        provided_pin = request.args.get("pin")
        if required_pin and provided_pin != required_pin:
            return render_template("results_locked.html")

        data = get_results()
        total = sum(data.values())
        rows = [(p, data.get(p, 0)) for p in parties]
        return render_template("results.html", rows=rows, total=total)

    return app




if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

print(" how is your expirience ")