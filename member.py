from flask import Blueprint, render_template, redirect, url_for, flash, g
from auth import login_required, role_required
from database import get_db

member_bp = Blueprint("member", __name__, url_prefix="/member")


@member_bp.route("/dashboard")
@login_required
@role_required("member")
def dashboard():
    return render_template("member/dashboard.html", user=g.user)


@member_bp.route("/books")
@login_required
@role_required("member")
def books():
    db = get_db()
    available_books = db.execute("SELECT * FROM books WHERE available=1").fetchall()
    borrowed_books = db.execute(
        """
        SELECT b.id, b.title, b.author FROM books b
        JOIN borrowed_books bb ON b.id = bb.book_id
        WHERE bb.user_id=?
    """,
        (g.user["id"],),
    ).fetchall()
    return render_template(
        "member/books.html",
        books=available_books,
        borrowed_books=borrowed_books,
        user=g.user,
    )


@member_bp.route("/borrow/<int:book_id>")
@login_required
@role_required("member")
def borrow_book(book_id):
    db = get_db()
    book = db.execute(
        "SELECT * FROM books WHERE id=? AND available=1", (book_id,)
    ).fetchone()
    if not book:
        flash("Book not available!")
        return redirect(url_for("member.books"))

    db.execute(
        "INSERT INTO borrowed_books (user_id, book_id) VALUES (?, ?)",
        (g.user["id"], book_id),
    )
    db.execute("UPDATE books SET available=0 WHERE id=?", (book_id,))
    db.commit()
    flash(f"You borrowed '{book['title']}' successfully!")
    return redirect(url_for("member.books"))


@member_bp.route("/return/<int:book_id>")
@login_required
@role_required("member")
def return_book(book_id):
    db = get_db()
    borrowed = db.execute(
        "SELECT * FROM borrowed_books WHERE user_id=? AND book_id=?",
        (g.user["id"], book_id),
    ).fetchone()
    if not borrowed:
        flash("You have not borrowed this book!")
        return redirect(url_for("member.books"))

    db.execute("DELETE FROM borrowed_books WHERE id=?", (borrowed["id"],))
    db.execute("UPDATE books SET available=1 WHERE id=?", (book_id,))
    db.commit()
    flash("Book returned successfully!")
    return redirect(url_for("member.books"))
