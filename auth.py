from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    make_response,
    g,
    current_app,
)
import jwt, datetime, bcrypt
from functools import wraps
from database import get_db

auth_bp = Blueprint("auth", __name__)


def create_jwt(user_id, username, role):
    payload = {
        "id": user_id,
        "user": username,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


def decode_jwt(token):
    try:
        return jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
    except:
        return None


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("access_token")
        data = decode_jwt(token) if token else None
        if not data:
            return redirect(url_for("auth.login"))
        g.user = data["user"]
        g.role = data["role"]
        g.user_id = data["id"]
        return f(*args, **kwargs)

    return decorated


def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.cookies.get("access_token")
            data = decode_jwt(token) if token else None
            if not data or data.get("role") != role:
                return "Unauthorized", 403
            g.user = data["user"]
            g.role = data["role"]
            g.user_id = data["id"]
            return f(*args, **kwargs)

        return decorated

    return decorator


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username=?", (request.form["username"],)
        ).fetchone()
        if user and bcrypt.checkpw(request.form["password"].encode(), user["password"]):
            token = create_jwt(user["id"], user["username"], user["role"])
            resp = make_response(redirect(url_for("dashboard")))
            resp.set_cookie("access_token", token, httponly=True)
            return resp
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        db = get_db()
        hashed = bcrypt.hashpw(request.form["password"].encode(), bcrypt.gensalt())
        db.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (request.form["username"], hashed, "member"),
        )
        db.commit()
        return redirect(url_for("auth.login"))
    return render_template("register.html")


@auth_bp.route("/logout")
def logout():
    resp = make_response(redirect(url_for("auth.login")))
    resp.delete_cookie("access_token")
    return resp
