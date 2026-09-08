import pytest
from flask import Flask, Response

def make_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    db = {
        'tesla': {'name': 'tesla', 'type': 'car'},
        'boeing': {'name': 'boeing', 'type': 'plane'},
        'yamaha': {'name': 'yamaha', 'type': 'bike'},
    }
    @app.route('/vehicles', methods=['GET'])
    def list_vehicles():
        names = ', '.join(db.keys())
        return f"vehicles: {names}"
    @app.route('/vehicles/<name>', methods=['GET'])
    def show_vehicle(name):
        vehicle = db.get(name)
        if not vehicle:
            return Response('cannot find that vehicle', status=404)
        return f"{vehicle['name']} is a {vehicle['type']}"
    return app

@pytest.fixture
def client():
    app = make_app()
    return app.test_client()

def test_get_vehicles_returns_list(client):
    resp = client.get('/vehicles')
    assert resp.status_code == 200
    assert resp.data.decode() == 'vehicles: tesla, boeing, yamaha'

def test_get_vehicles_name_returns_info(client):
    resp = client.get('/vehicles/tesla')
    assert resp.status_code == 200
    assert resp.data.decode() == 'tesla is a car'
    resp = client.get('/vehicles/yamaha')
    assert resp.status_code == 200
    assert resp.data.decode() == 'yamaha is a bike'

def test_get_vehicles_name_not_found_returns_404(client):
    resp = client.get('/vehicles/unknown')
    assert resp.status_code == 404
    assert resp.data.decode() == 'cannot find that vehicle'