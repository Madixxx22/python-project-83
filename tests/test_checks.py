import pytest
from page_analyzer.validators import validate_url
from page_analyzer.logic_checks import check_response


@pytest.fixture()
def data_validators():
    urls = {
        "success": {"url": "https://google.com", "error": "valid"},
        "long": {"url": "https://gooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooogle.com", "error": "exceeded size"},  # noqa: E501 pylint: disable=unused-variable
        "zero": {"url": "", "error": "zero size"},
        "not valid": {"url": "https://google", "error": "not valid"}
    }
    return urls


@pytest.fixture()
def data():
    urls_results = {
        "urls": {
            "success": "https://ru.hexlet.io",
            "error": "errorsite.ru"
        },
        "results": {
            "success": [
                200,
                "Онлайн-школа программирования, за выпускниками которой охотятся компании\n",  # noqa: E501 pylint: disable=unused-variable
                "Хекслет — больше чем школа программирования. Онлайн курсы, сообщество программистов",  # noqa: E501 pylint: disable=unused-variable
                "Живое онлайн сообщество программистов и разработчиков на JS, Python, Java, PHP, Ruby. Авторские программы обучения с практикой и готовыми проектами в резюме. Помощь в трудоустройстве после успешного окончания обучения"  # noqa: E501 pylint: disable=unused-variable
                ],
            "error": [404, True]
        }
    }

    return urls_results


def test_check_success(data):
    response = check_response(data["urls"]["success"])
    assert response["status_code"] in data["results"]["success"]
    assert response["h1"] in data["results"]["success"]
    assert response["title"] in data["results"]["success"]
    assert response["meta"] in data["results"]["success"]


def test_check_error(data):
    response = check_response(data["urls"]["error"])
    assert response["error"] in data["results"]["error"]


def test_validate_success(data_validators):
    response = validate_url(data_validators["success"]["url"])
    assert data_validators["success"]["error"] in response["status"]


def test_validate_long(data_validators):
    response = validate_url(data_validators["long"]["url"])
    assert data_validators["long"]["error"] in response["status"]


def test_validate_zero(data_validators):
    response = validate_url(data_validators["zero"]["url"])
    assert data_validators["zero"]["error"] in response["status"]


def test_validate_not_valid(data_validators):
    response = validate_url(data_validators["not valid"]["url"])
    assert data_validators["not valid"]["error"] in response["status"]
