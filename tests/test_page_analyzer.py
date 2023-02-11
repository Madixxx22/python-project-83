import pytest
from page_analyzer.app import app


@pytest.fixture()
def get_app():
    app.config.update({"TESTING": True})
    yield app


@pytest.fixture()
def client(get_app):
    return get_app.test_client()


def test_request_example(client):
    response = client.get('/')
    print(response)
