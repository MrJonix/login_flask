from flask import Flask, request, render_template, make_response
import hashlib

app = Flask(__name__)

# Credentials for the login
valid_credentials = {
    "user": "password",
    "admin": "3s1$tB€vö1k€rungW€$ha1bCHFKurzfri5tig"
}

# Function to generate an MD5 hash
def generate_md5_hash(data):
    return hashlib.md5(data.encode()).hexdigest()

@app.route("/")
def index():
    # Retrieve the session cookie value from the request cookies
    session_cookie = request.cookies.get('session_cookie')
    
    # Check if the session cookie is present and matches the expected value
    if session_cookie and any(session_cookie == generate_md5_hash(username) for username in valid_credentials):
        # Get the actual username from the valid_credentials dictionary
        username = [k for k, v in valid_credentials.items() if session_cookie == generate_md5_hash(k)][0]
        
        # User is authenticated, render the desired page (e.g., dashboard)
        if(username == "admin"):
            return render_template("success.html", username=username, admin= "Congratulations! You've successfully conquered the challenges and emerged victorious in the CTF. Well done! 🎉🔐")
        return render_template("success.html", username=username)
        
    else:
        # User is not authenticated, render the login page with an error message
        return render_template("login.html", error="")

@app.route("/", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if username in valid_credentials and password == valid_credentials[username]:
        # If credentials are valid, generate an MD5 hash and set it as a session cookie
        session_cookie = generate_md5_hash(username)
        response = make_response(render_template("success.html", username=username))
        response.set_cookie("session_cookie", session_cookie)
        return response
    else:
        return render_template("login.html", error="Invalid credentials. Please try again.")

if __name__ == "__main__":
    app.run(debug=True)
