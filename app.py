import os
from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
from functools import wraps
from models import app, db, User, Post

# Конфигурация загрузки изображений
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Убедись, что папка существует
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

migrate = Migrate(app, db)

# Декоратор авторизации
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You must be logged in.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@login_required
def home():
    user = User.query.get(session['user_id'])
    posts = Post.query.filter_by(user_id=user.id).all()
    return render_template('dashboard.html', user=user, posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash('Fields cannot be empty.')
            return redirect(url_for('register'))
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('User already exists!')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('User registered successfully!')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful!')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials!')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have logged out.')
    return redirect(url_for('login'))

@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    if request.method == 'POST':
        title = request.form['title'].strip()
        content = request.form['content'].strip()
        image = request.files.get('image')

        if not title or not content:
            flash('Title and content cannot be empty.')
            return redirect(url_for('add_post'))

        image_filename = None
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            image_filename = filename

        post = Post(title=title, content=content, image_filename=image_filename, user_id=session['user_id'])
        db.session.add(post)
        db.session.commit()
        flash('Post successfully added!')
        return redirect(url_for('home'))

    return render_template('add_post.html')

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != session['user_id']:
        flash('You do not have permission to edit this post.')
        return redirect(url_for('home'))

    if request.method == 'POST':
        post.title = request.form['title'].strip()
        post.content = request.form['content'].strip()
        if not post.title or not post.content:
            flash('Fields cannot be empty.')
            return redirect(url_for('edit_post', post_id=post_id))

        db.session.commit()
        flash('Post updated.')
        return redirect(url_for('home'))

    return render_template('edit_post.html', post=post)

@app.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != session['user_id']:
        flash('You cannot delete this post.')
        return redirect(url_for('home'))

    if post.image_filename:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], post.image_filename)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(post)
    db.session.commit()
    flash('Post deleted.')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
