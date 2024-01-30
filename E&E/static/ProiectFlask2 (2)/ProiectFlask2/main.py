from flask import Flask, render_template

app = Flask(__name__)


@app.route("/home")
@app.route("/") ## this is so that with both notations the same page is accessed
def home():
    return render_template("home.html")


@app.route("/signup")
@app.route("/sign-up") ## this is so that with both notations the same page is accessed
def signup():
    return render_template("sign-up.html")


if __name__ == "__main__":
    app.run(debug=True)