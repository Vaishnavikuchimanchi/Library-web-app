import sqlite3
import bcrypt

DB = "library.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    db = get_db()
    cur = db.cursor()

    # Users table
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password BLOB,
        role TEXT
    )
    """
    )

    # Books table
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        available INTEGER
    )
    """
    )

    # Borrowed books table
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS borrowed_books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        book_id INTEGER,
        borrowed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    )

    # Seed admin
    admin_pass = bcrypt.hashpw(b"admin123", bcrypt.gensalt())
    cur.execute(
        "INSERT OR IGNORE INTO users (username,password,role) VALUES (?,?,?)",
        ("admin", admin_pass, "admin"),
    )

    # Seed member
    member_pass = bcrypt.hashpw(b"member123", bcrypt.gensalt())
    cur.execute(
        "INSERT OR IGNORE INTO users (username,password,role) VALUES (?,?,?)",
        ("john", member_pass, "member"),
    )

    # Seed books
    books = [
        ("The Alchemist", "Paulo Coelho", 1),
        ("1984", "George Orwell", 1),
        ("To Kill a Mockingbird", "Harper Lee", 1),
        ("Pride and Prejudice", "Jane Austen", 1),
        ("Harry Potter and the Sorcerer's Stone", "J.K. Rowling", 1),
    ]
    for title, author, available in books:
        cur.execute(
            "INSERT OR IGNORE INTO books (title, author, available) VALUES (?, ?, ?)",
            (title, author, available),
        )

    db.commit()
    db.close()
    print("Database initialized.")
