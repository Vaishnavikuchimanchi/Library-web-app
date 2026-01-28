from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    make_response,
    flash,
)
from database import init_db, get_db
import bcrypt
from auth import create_jwt, decode_jwt
from admin import admin_bp
from member import member_bp

app = Flask(__name__)
app.secret_key = "super-secret-key"

# Register Blueprints
app.register_blueprint(admin_bp)
app.register_blueprint(member_bp)

# Initialize DB
init_db()


# ----------------- Public Routes -----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = "member"
        db = get_db()
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        try:
            db.execute(
                "INSERT INTO users (username,password,role) VALUES (?,?,?)",
                (username, hashed, role),
            )
            db.commit()
            flash("Registration successful! Login now.")
            return redirect(url_for("login"))
        except:
            flash("Username already exists!")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"].encode()
        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username=?", (username,)
        ).fetchone()
        if user and bcrypt.checkpw(password, user["password"]):
            token = create_jwt(user["id"], user["username"], user["role"])
            resp = make_response(redirect(url_for(f"{user['role']}.dashboard")))
            resp.set_cookie("access_token", token, httponly=True, samesite="Lax")
            return resp
        flash("Invalid credentials!")
    return render_template("login.html")


@app.route("/logout")
def logout():
    resp = make_response(redirect(url_for("login")))
    resp.delete_cookie("access_token")
    flash("Logged out successfully!")
    return resp


if __name__ == "__main__":
    app.run(debug=True)
