import types
import pytest

import gigachat
from gigachat.models import Chat, Messages, MessagesRole


@pytest.fixture
def fake_gigachat(monkeypatch):
    class MockChoices:
        def __init__(self, message):
            self.message = message

    class MockResponse:
        def __init__(self, content):
            self.choices = [MockChoices(message=types.SimpleNamespace(content=content))]
    # Patch GigaChat.__enter__ and __exit__
    class DummyGigaChat:
        def __init__(self, *args, **kwargs):
            self.messages = []

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def chat(self, payload):
            # Return a mock response
            return MockResponse("test-response")

        def embeddings(self, texts):
            return ["embedding-1", "embedding-2"]

    monkeypatch.setattr(gigachat, "GigaChat", DummyGigaChat)
    return DummyGigaChat


def test_example_ask(fake_gigachat, capsys):
    from gigachat import GigaChat
    with GigaChat(credentials="fake", verify_ssl_certs=False) as giga:
        response = giga.chat("What?")
        assert response.choices[0].message.content == "test-response"

def test_example_embeddings(fake_gigachat, capsys):
    from gigachat import GigaChat
    with GigaChat(credentials="fake", verify_ssl_certs=False) as giga:
        resp = giga.embeddings(["Hello world!"])
        assert resp == ["embedding-1", "embedding-2"]

def test_example_russian_trusted_root_ca(fake_gigachat, capsys):
    from gigachat import GigaChat
    with GigaChat(credentials="fake", ca_bundle_file="cert.cer") as giga:
        resp = giga.chat("Test?")
        assert resp.choices[0].message.content == "test-response"

def test_simple_chat_loop(fake_gigachat, monkeypatch, capsys):
    from gigachat import GigaChat
    from gigachat.models import Chat, Messages, MessagesRole

    payload = Chat(
        messages=[
            Messages(
                role=MessagesRole.SYSTEM,
                content="Ты внимательный бот-психолог, который помогает пользователю решить его проблемы."
            )
        ],
        temperature=0.7,
        max_tokens=100,
    )

    input_values = ["Привет!", "exit"]
    def mock_input(prompt):
        return input_values.pop(0)

    monkeypatch.setattr("builtins.input", mock_input)
    with GigaChat(credentials="fake", verify_ssl_certs=False) as giga:
        count = 0
        while True:
            user_input = input("User: ")
            if user_input == "exit":
                break
            payload.messages.append(Messages(role=MessagesRole.USER, content=user_input))
            response = giga.chat(payload)
            payload.messages.append(response.choices[0].message)
            print("Bot: ", response.choices[0].message.content)
            count += 1
        assert count == 1

def test_example_contextvars(fake_gigachat, monkeypatch, capsys):
    import gigachat.context as ctx
    from gigachat import GigaChat

    ACCESS_TOKEN = "test123"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "X-Session-ID": "8324244b-7133-4d30-a328-31d8466e5502",
        "X-Request-ID": "8324244b-7133-4d30-a328-31d8466e5502",
        "X-Service-ID": "my_custom_service",
        "X-Operation-ID": "my_custom_qna",
    }

    with GigaChat(verify_ssl_certs=False) as giga:
        ctx.authorization_cvar.set(headers.get("Authorization"))
        ctx.session_id_cvar.set(headers.get("X-Session-ID"))
        ctx.request_id_cvar.set(headers.get("X-Request-ID"))
        ctx.service_id_cvar.set(headers.get("X-Service-ID"))
        ctx.operation_id_cvar.set(headers.get("X-Operation-ID"))

        response = giga.chat("Какие факторы влияют на стоимость страховки на дом?")
        assert response.choices[0].message.content == "test-response"