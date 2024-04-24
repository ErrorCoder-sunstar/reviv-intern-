from flask import Flask, render_template, request, url_for, redirect, flash, session, abort
import firebase_admin
from firebase_admin import credentials, auth

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = '1daaef91ea714255b095341b8bc311fc'  # Update with a strong secret key

# Initialize Firebase Admin SDK
cred = credentials.Certificate('credentials.json')
firebase_admin.initialize_app(cred)

@app.route("/signup/", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        try:
            user = auth.create_user(email=username, password=password)
            flash("User account has been created.")
            return redirect(url_for("login"))
        except Exception as e:
            flash("Failed to create user account: {}".format(e))
            return redirect(url_for('signup'))

    return render_template("signup.html")

@app.route("/", methods=["GET", "POST"])
@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        try:
            user = auth.get_user_by_email(username)
            if user and auth.verify_password(password, user.password_hash):
                session[username] = True
                return redirect(url_for("user_home", username=username))
            else:
                flash("Invalid username or password.")
                return redirect(url_for('login'))
        except Exception as e:
            flash("Failed to authenticate user: {}".format(e))
            return redirect(url_for('login'))

    return render_template("login_form.html")

@app.route("/user/<username>/")
def user_home(username):
    if not session.get(username):
        abort(401)

    return render_template("user_home.html", username=username)

@app.route("/logout/<username>")
def logout(username):
    session.pop(username, None)
    flash("Successfully logged out.")
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(port=5000, debug=True)
