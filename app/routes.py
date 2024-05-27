# app/routes.py
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from app.models import Recipe, Comment, User

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/submit_recipe', methods=['GET', 'POST'])
def submit_recipe():
    if request.method == 'POST':
        title = request.form['title']
        image_url = request.form['image_url']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']

        new_recipe = Recipe(title=title, image_url=image_url, ingredients=ingredients, instructions=instructions)
        db.session.add(new_recipe)
        db.session.commit()

        flash('Recipe submitted successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('submit_recipe.html')

@app.route('/recipe/<int:recipe_id>', methods=['GET', 'POST'])
def view_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if request.method == 'POST':
        rating = float(request.form['rating'])

        recipe.rating = (recipe.rating * recipe.num_ratings + rating) / (recipe.num_ratings + 1)
        recipe.num_ratings += 1

        db.session.commit()

        flash('Thank you for rating the recipe!', 'success')

    return render_template('view_recipe.html', recipe=recipe)

@app.route('/rate_recipe/<int:recipe_id>', methods=['POST'])
def rate_recipe(recipe_id):
    pass  # The rating logic is already implemented in the view_recipe route

@app.route('/comment/<int:recipe_id>', methods=['POST'])
def comment(recipe_id):
    if request.method == 'POST':
        content = request.form['content']

        new_comment = Comment(content=content, recipe_id=recipe_id)
        db.session.add(new_comment)
        db.session.commit()

        flash('Comment added successfully!', 'success')

    return redirect(url_for('view_recipe', recipe_id=recipe_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))
