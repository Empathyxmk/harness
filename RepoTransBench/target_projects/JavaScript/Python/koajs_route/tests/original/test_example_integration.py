import pytest
from flask import Flask, Response

@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True
    db = {
        'tobi': {'name': 'tobi', 'species': 'ferret'},
        'loki': {'name': 'loki', 'species': 'ferret'},
        'jane': {'name': 'jane', 'species': 'ferret'},
    }

    @app.route('/pets', methods=['GET'])
    def list_pets():
        names = ', '.join(db.keys())
        return f"pets: {names}"

    @app.route('/pets/<name>', methods=['GET'])
    def show_pet(name):
        pet = db.get(name)
        if not pet:
            return Response('cannot find that pet', status=404)
        return f"{pet['name']} is a {pet['species']}"

    return app.test_client()

def test_get_pets_returns_list(client):
    resp = client.get('/pets')
    assert resp.status_code == 200
    assert resp.data.decode() == 'pets: tobi, loki, jane'

def test_get_pets_name_returns_info(client):
    resp = client.get('/pets/tobi')
    assert resp.status_code == 200
    assert resp.data.decode() == 'tobi is a ferret'
    resp = client.get('/pets/loki')
    assert resp.status_code == 200
    assert resp.data.decode() == 'loki is a ferret'

def test_get_pets_name_not_found_returns_404(client):
    resp = client.get('/pets/unknown')
    assert resp.status_code == 404
    assert resp.data.decode() == 'cannot find that pet'