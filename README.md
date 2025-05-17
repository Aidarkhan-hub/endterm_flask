# 📝 Flask Post Management App

A minimal and functional web application built with **Flask**, **SQLite**, and **Jinja2** that allows users to register, log in, create, edit, and delete posts with optional image uploads.

---

## 🔍 Features

- 🔐 **User Authentication**
  - Register / Login / Logout
  - Passwords are securely hashed using `werkzeug.security`

- 🖼️ **Post Management**
  - Add, edit, delete posts
  - Image upload with preview and size limit (max 2MB)

- 📁 **Profile & Feed**
  - See your own posts on `/profile`
  - Browse others’ posts on `/feed`

- 🔒 **Access Control**
  - Protected routes using a custom `@login_required` decorator
  - Only the author can edit or delete their posts

- 📦 **File Uploads**
  - Supported file types: JPG, PNG, GIF
  - Stored in `/static/uploads/`

- ⚙️ **Extras**
  - Flash notifications
  - Bootstrap-like styling with clean layout
  - JavaScript validation + image preview
  - Context-aware navbar

---

## 🗃️ Project Structure
endterm_flask/
├── static/
│ └── uploads/ # Uploaded images
├── templates/
│ ├── base.html
│ ├── login.html
│ ├── register.html
│ ├── dashboard.html
│ ├── add_post.html
│ ├── edit_post.html
│ ├── profile.html
│ └── feed.html
├── app.py # Main application logic
├── models.py # SQLAlchemy models
├── requirements.txt
└── README.md # This file

Install dependencies
pip install -r requirements.txt

Initialize DB
flask db init
flask db migrate -m "Initial migration"
flask db upgrade


Run the server
flask run

ER Diagram
User
----
id (PK)
username
password

Post
----
id (PK)
title
content
image_filename
user_id (FK → User.id)




