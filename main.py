from flask import Flask, request, render_template, make_response
import hashlib

app = Flask(__name__)

# Credentials for the login
valid_username = "admin"
valid_password = "password"

# Function to generate an MD5 hash
def generate_md5_hash(data):
    return hashlib.md5(data.encode()).hexdigest()

@app.route("/")
def index():
    # Retrieve the session cookie value from the request cookies
    session_cookie = request.cookies.get('session_cookie')
    # Check if the session cookie is present and matches the expected value
    if session_cookie and session_cookie == generate_md5_hash(valid_username):
        # User is authenticated, render the desired page (e.g., dashboard)
        return render_template("success.html", username=valid_username)
    else:
        # User is not authenticated, render the login page with an error message
        return render_template("login.html", error="")


@app.route("/", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if username == valid_username and password == valid_password:
        # If credentials are valid, generate an MD5 hash and set it as a session cookie
        session_cookie = generate_md5_hash(username)
        response = make_response(render_template("success.html", username=username))
        response.set_cookie("session_cookie", session_cookie)
        return response
    else:
        return render_template("login.html", error="Invalid credentials. Please try again.")


if __name__ == "__main__":
    app.run(debug=True)