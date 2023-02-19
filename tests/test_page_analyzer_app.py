import pytest
from page_analyzer.app import app


@pytest.fixture()
def get_app():
    app.config.update({"TESTING": True})
    yield app


@pytest.fixture()
def client(get_app):
    return get_app.test_client()


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'Анализатор страниц' in response.text
    assert 'Бесплатно проверяйте сайты на SEO пригодность' in response.text


def test_request_404(client):
    reponse = client.get('/example')
    assert reponse.status_code == 404
    assert 'Страница не найдена' in reponse.text
