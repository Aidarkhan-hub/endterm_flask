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

