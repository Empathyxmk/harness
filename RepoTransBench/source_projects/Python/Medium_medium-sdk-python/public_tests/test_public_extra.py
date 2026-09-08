import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from medium import Client

def test_client_init_public():
    c = Client('public_token_abc')
    assert c.token == 'public_token_abc'