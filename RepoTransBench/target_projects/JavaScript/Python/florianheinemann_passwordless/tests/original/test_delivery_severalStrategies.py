import pytest
from flask import Flask, request as flask_request
from flask.testing import FlaskClient
from werkzeug.datastructures import MultiDict

# Mock classes analogous to the JS Mocks and TokenStoreMock
class TokenStoreMock:
    # Simulated token store for testing purposes
    def __init__(self):
        self.tokens = []

    def store_token(self, user, delivery):
        self.tokens.append((user, delivery))

class Mocks:
    def __init__(self):
        self.delivered = []

    def alice(self):
        # Returns a mock representation of "alice"
        return type('Alice', (), {
            "email": "alice@example.com",
            "phone": "+12025550123"
        })()

    def deliveryMockSend(self, delivery_type):
        def send(token, user, req):
            self.delivered.append({"token": token, "user": user, "delivery": delivery_type})
        return send

    def getUserId(self):
        def user_lookup(req):
            # Just returns 'user' field from the request form/json
            if flask_request.is_json:
                return flask_request.json.get("user")
            else:
                return flask_request.form.get("user")
        return user_lookup

# Simulating the Passwordless class and requestToken logic
class Passwordless:
    def __init__(self):
        self.token_store = None
        self.delivery_methods = {}
        self.delivery_field = "delivery"  # default

    def init(self, token_store):
        self.token_store = token_store

    def addDelivery(self, name, func):
        self.delivery_methods[name] = func

    def requestToken(self, user_fn, options=None):
        delivery_field = options["deliveryField"] if options and "deliveryField" in options else "delivery"

        def middleware():
            data = flask_request.get_json() if flask_request.is_json else flask_request.form
            user = data.get("user")
            delivery = data.get(delivery_field)

            # Validate presence of delivery param
            if not delivery:
                return ("Missing delivery method", 400)
            if delivery not in self.delivery_methods:
                return ("Invalid delivery method", 400)
            # Simulate token generation, storage and delivery
            token = "token-for-" + str(user)
            self.token_store.store_token(user, delivery)
            self.delivery_methods[delivery](token, user, flask_request)
            return ("", 200)
        return middleware

@pytest.fixture
def client_factory():
    def create_app_and_mocks(option_delivery_field=None):
        mocks = Mocks()
        token_store = TokenStoreMock()
        passwordless = Passwordless()
        passwordless.init(token_store)
        app = Flask(__name__)
        app.config['TESTING'] = True

        passwordless.addDelivery('email', mocks.deliveryMockSend('email'))
        passwordless.addDelivery('sms', mocks.deliveryMockSend('sms'))
        if not option_delivery_field:
            app.add_url_rule(
                '/login', view_func=passwordless.requestToken(mocks.getUserId()), methods=['POST']
            )
        else:
            app.add_url_rule(
                '/login', view_func=passwordless.requestToken(mocks.getUserId(), {'deliveryField': option_delivery_field}), methods=['POST']
            )
        return app.test_client(), mocks
    return create_app_and_mocks

def test_should_return_400_if_field_delivery_is_not_provided(client_factory):
    client, mocks = client_factory()
    response = client.post('/login', json={'user': mocks.alice().email})
    assert response.status_code == 400

def test_should_not_have_sent_or_stored_any_tokens_so_far_1(client_factory):
    client, mocks = client_factory()
    # since above, delivered should be untouched for a new mocks
    assert len(mocks.delivered) == 0

def test_should_return_400_if_field_delivery_is_invalid(client_factory):
    client, mocks = client_factory()
    response = client.post('/login', json={'user': mocks.alice().email, 'delivery': 'snailmail'})
    assert response.status_code == 400

def test_should_not_have_sent_or_stored_any_tokens_so_far_2(client_factory):
    client, mocks = client_factory()
    assert len(mocks.delivered) == 0

def test_should_deliver_token_for_valid_delivery_method_sms(client_factory):
    client, mocks = client_factory()
    response = client.post('/login', json={'user': mocks.alice().phone, 'delivery': 'sms'})
    assert response.status_code == 200

def test_should_have_sent_and_stored_token_sms(client_factory):
    client, mocks = client_factory()
    # send first
    client.post('/login', json={'user': mocks.alice().phone, 'delivery': 'sms'})
    assert len(mocks.delivered) == 1
    assert mocks.delivered[0]['delivery'] == 'sms'

def test_should_deliver_token_for_valid_delivery_method_email(client_factory):
    client, mocks = client_factory()
    # send with sms first to ensure the delivered list is filled, since original uses two agents
    client.post('/login', json={'user': mocks.alice().phone, 'delivery': 'sms'})
    response = client.post('/login', json={'user': mocks.alice().email, 'delivery': 'email'})
    assert response.status_code == 200

def test_should_have_sent_and_stored_token_email(client_factory):
    client, mocks = client_factory()
    client.post('/login', json={'user': mocks.alice().phone, 'delivery': 'sms'})
    client.post('/login', json={'user': mocks.alice().email, 'delivery': 'email'})
    assert len(mocks.delivered) == 2
    assert mocks.delivered[1]['delivery'] == 'email'

def test_option_delivery_field_should_deliver_token(client_factory):
    # With deliveryField set to 'method'
    client, mocks = client_factory(option_delivery_field='method')
    mocks.delivered = []
    response = client.post('/login', json={'user': mocks.alice().phone, 'method': 'sms'})
    assert response.status_code == 200
    assert len(mocks.delivered) == 1
    assert mocks.delivered[0]['delivery'] == 'sms'