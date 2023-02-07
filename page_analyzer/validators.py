from validators.url import url
from page_analyzer.database import get_id_url_by_name


def is_null(value: any) -> bool:
    if value == []:
        return True
    elif value is None:
        return True
    elif value == '':
        return True
    elif len(value) == 0:
        return True
    return False


def validate_url(check_url: str) -> dict:
    errors = {
        'url': get_id_url_by_name(check_url),
        'status': []
    }
    if len(check_url) >= 255:
        errors['status'].append('exceeded size')
    elif len(check_url) == 0:
        errors['status'].append('zero size')
    if not url(check_url):
        errors['status'].append('not valid')
        return errors
    if not is_null(errors['url']):
        errors['status'].append('exists')
        errors['status'].append('not valid')
        return errors
    errors['status'].append('valid')
    return errors
