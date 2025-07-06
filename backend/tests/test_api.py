"""Basic API tests using Flask test client."""

import os
import tempfile
import json
import pytest
from app import app, db, Recipe

@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
    client = app.test_client()
    yield client
    os.close(db_fd)
    os.unlink(db_path)


def test_create_and_get_recipe(client):
    """Create a recipe and fetch it."""
    response = client.post('/api/recipes', json={
        'title': 'Salad',
        'description': 'Fresh',
        'ingredients': ['lettuce', 'tomato']
    })
    assert response.status_code == 201
    data = response.get_json()
    recipe_id = data['id']

    get_resp = client.get(f'/api/recipes/{recipe_id}')
    assert get_resp.status_code == 200
    get_data = get_resp.get_json()
    assert get_data['title'] == 'Salad'
    assert 'lettuce' in get_data['ingredients']


def test_rating(client):
    """Rate a recipe."""
    resp = client.post('/api/recipes', json={'title': 'Soup'})
    recipe_id = resp.get_json()['id']
    rate_resp = client.post(f'/api/recipes/{recipe_id}/rating', json={'score': 5})
    assert rate_resp.status_code == 201
    assert rate_resp.get_json()['score'] == 5
