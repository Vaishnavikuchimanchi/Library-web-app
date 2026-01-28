# 📚 Library Management Web Application

A server-rendered Library Management System built with **Flask**, featuring **JWT-based authentication**, **role-based authorization**, and **secure access control**. Users interact through HTML pages (no REST APIs). The system supports two roles: **Admin** and **Member**.

---

## 🚀 Features

### Authentication & Authorization
- Secure login and registration with **hashed passwords** (bcrypt).
- **JWT-based authentication** stored in **HTTP-only cookies**.
- Role-based access control:
  - **Admin**: Manage books, view all book details, access admin dashboard.
  - **Member**: View available books, access member dashboard.
- Logout invalidates JWT session.

### Access Control
- Page-level and action-level restrictions.
- Unauthenticated users are redirected to the login page.

### Storage
- **SQLite3** database (raw SQL, no ORM).
- Persistent storage for users and books.

### Frontend
- **Jinja2 templates** for server-side rendering.
- Minimal **HTML + CSS** (no frontend frameworks).
- Responsive and simple UI.

---

## 🛠️ Technology Stack

- **Python 3.x**
- **Flask**
- **Flask-JWT-Extended**
- **SQLite3**
- **bcrypt**
- **Jinja2**
- **HTML + CSS**

---

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/Vaishnavikuchimanchi/Library-web-app
cd library_app

Install dependencies
pip install -r requirements.txt

Run the application
python app.py

User Roles
Admin
- Login to admin dashboard.
- Add new books.
- View all book details.
Member
- Login to member dashboard.
- View available books.
