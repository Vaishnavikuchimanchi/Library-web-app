from flask import Blueprint, render_template, redirect, url_for, request, flash, g
from auth import login_required, role_required
from database import get_db

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/dashboard")
@login_required
@role_required("admin")
def dashboard():
    return render_template("admin/dashboard.html", user=g.user)


@admin_bp.route("/books")
@login_required
@role_required("admin")
def books():
    db = get_db()
    books = db.execute("SELECT * FROM books").fetchall()
    return render_template("admin/books.html", books=books, user=g.user)


@admin_bp.route("/books/add", methods=["GET", "POST"])
@login_required
@role_required("admin")
def add_book():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        db = get_db()
        db.execute(
            "INSERT INTO books (title, author, available) VALUES (?, ?, 1)",
            (title, author),
        )
        db.commit()
        flash("Book added successfully!")
        return redirect(url_for("admin.books"))
    return render_template("admin/add_book.html", user=g.user)


@admin_bp.route("/books/edit/<int:book_id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def edit_book(book_id):
    db = get_db()
    book = db.execute("SELECT * FROM books WHERE id=?", (book_id,)).fetchone()
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        db.execute(
            "UPDATE books SET title=?, author=? WHERE id=?", (title, author, book_id)
        )
        db.commit()
        flash("Book updated successfully!")
        return redirect(url_for("admin.books"))
    return render_template("admin/edit_book.html", book=book, user=g.user)


@admin_bp.route("/books/delete/<int:book_id>")
@login_required
@role_required("admin")
def delete_book(book_id):
    db = get_db()
    db.execute("DELETE FROM books WHERE id=?", (book_id,))
    db.commit()
    flash("Book deleted successfully!")
    return redirect(url_for("admin.books"))


@admin_bp.route("/borrowed")
@login_required
@role_required("admin")
def borrowed_history():
    db = get_db()
    borrowed = db.execute(
        """
        SELECT bb.id, u.username, b.title, b.author, bb.borrowed_at
        FROM borrowed_books bb
        JOIN users u ON bb.user_id = u.id
        JOIN books b ON bb.book_id = b.id
        ORDER BY bb.borrowed_at DESC
    """
    ).fetchall()
    return render_template("admin/borrowed.html", borrowed=borrowed, user=g.user)
