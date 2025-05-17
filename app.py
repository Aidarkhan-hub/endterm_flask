from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from functools import wraps
from models import app, db, User, Post

migrate = Migrate(app, db)

# Декоратор авторизации
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Вы должны войти в систему.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

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
            flash('Поля не должны быть пустыми.')
            return redirect(url_for('register'))
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Пользователь уже существует!')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Пользователь успешно зарегистрирован!')
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
            flash('Успешный вход!')
            return redirect(url_for('home'))
        else:
            flash('Неверные данные!')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Вы вышли из системы.')
    return redirect(url_for('login'))

@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    if request.method == 'POST':
        title = request.form['title'].strip()
        content = request.form['content'].strip()
        if not title or not content:
            flash('Поля "Заголовок" и "Содержание" не могут быть пустыми.')
            return redirect(url_for('add_post'))

        post = Post(title=title, content=content, user_id=session['user_id'])
        db.session.add(post)
        db.session.commit()
        flash('Пост успешно добавлен!')
        return redirect(url_for('home'))

    return render_template('add_post.html')

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != session['user_id']:
        flash('У вас нет доступа к этому посту.')
        return redirect(url_for('home'))

    if request.method == 'POST':
        post.title = request.form['title'].strip()
        post.content = request.form['content'].strip()
        if not post.title or not post.content:
            flash('Поля не могут быть пустыми.')
            return redirect(url_for('edit_post', post_id=post_id))

        db.session.commit()
        flash('Пост обновлён.')
        return redirect(url_for('home'))

    return render_template('edit_post.html', post=post)

@app.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != session['user_id']:
        flash('Вы не можете удалить этот пост.')
        return redirect(url_for('home'))

    db.session.delete(post)
    db.session.commit()
    flash('Пост удалён.')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
