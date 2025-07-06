"""Flask application entry point with API routes."""

import os
from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Flask app and configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Setup extensions
CORS(app)
db = SQLAlchemy(app)

# Simple root route to show API is running
@app.route('/')
def index():
    """Return a basic message for the API root."""
    return jsonify({
        'message': 'iRecipe API',
        'usage': 'Run the React frontend separately to use the web app.'
    })

# Association table between recipes and ingredients
recipe_ingredients = db.Table(
    'recipe_ingredients',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'))
)

class Recipe(db.Model):
    """Recipe model."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    images = db.relationship('RecipeImage', backref='recipe', lazy=True)
    ratings = db.relationship('Rating', backref='recipe', lazy=True)
    ingredients = db.relationship('Ingredient', secondary=recipe_ingredients, backref='recipes')

class Ingredient(db.Model):
    """Ingredient model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

class Rating(db.Model):
    """Rating model."""
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

class RecipeImage(db.Model):
    """RecipeImage model stores uploaded image path."""
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(200), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

def serialize_recipe(recipe):
    """Helper to convert recipe instance to dictionary."""
    return {
        'id': recipe.id,
        'title': recipe.title,
        'description': recipe.description,
        'ingredients': [i.name for i in recipe.ingredients],
        'images': [img.path for img in recipe.images],
        'ratings': [r.score for r in recipe.ratings]
    }

@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    """Return all recipes."""
    recipes = Recipe.query.all()
    return jsonify([serialize_recipe(r) for r in recipes])

@app.route('/api/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    """Return a single recipe."""
    recipe = Recipe.query.get_or_404(recipe_id)
    return jsonify(serialize_recipe(recipe))

@app.route('/api/recipes', methods=['POST'])
def create_recipe():
    """Create a new recipe."""
    data = request.json
    recipe = Recipe(title=data['title'], description=data.get('description'))
    ingredient_names = data.get('ingredients', [])
    for name in ingredient_names:
        ingredient = Ingredient.query.filter_by(name=name).first()
        if not ingredient:
            ingredient = Ingredient(name=name)
        recipe.ingredients.append(ingredient)
    db.session.add(recipe)
    db.session.commit()
    return jsonify(serialize_recipe(recipe)), 201

@app.route('/api/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    """Update an existing recipe."""
    recipe = Recipe.query.get_or_404(recipe_id)
    data = request.json
    recipe.title = data.get('title', recipe.title)
    recipe.description = data.get('description', recipe.description)
    if 'ingredients' in data:
        recipe.ingredients.clear()
        for name in data['ingredients']:
            ingredient = Ingredient.query.filter_by(name=name).first()
            if not ingredient:
                ingredient = Ingredient(name=name)
            recipe.ingredients.append(ingredient)
    db.session.commit()
    return jsonify(serialize_recipe(recipe))

@app.route('/api/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    """Delete a recipe."""
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return '', 204

@app.route('/api/recipes/<int:recipe_id>/rating', methods=['POST'])
def rate_recipe(recipe_id):
    """Add a rating to a recipe."""
    recipe = Recipe.query.get_or_404(recipe_id)
    data = request.json
    rating = Rating(score=int(data['score']), recipe=recipe)
    db.session.add(rating)
    db.session.commit()
    return jsonify({'score': rating.score}), 201

@app.route('/api/recipes/<int:recipe_id>/images', methods=['POST'])
def upload_image(recipe_id):
    """Upload an image and store its path."""
    recipe = Recipe.query.get_or_404(recipe_id)
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    file = request.files['image']
    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)
    img = RecipeImage(path=filename, recipe=recipe)
    db.session.add(img)
    db.session.commit()
    return jsonify({'path': filename}), 201

@app.route('/uploads/<path:filename>')
def get_image(filename):
    """Serve uploaded images."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    # Create tables if they do not exist
    with app.app_context():
        db.create_all()
    app.run(debug=True)
