import os
import requests
import datetime
from dotenv import load_dotenv
from flask import (
                  Flask,
                  render_template,
                  request,
                  redirect,
                  url_for,
                  flash,
                  get_flashed_messages
                 )
from page_analyzer.database import (
                                    get_urls,
                                    create_url,
                                    get_url_by_id,
                                    get_id_url_by_name,
                                    get_name_url_by_id,
                                    create_check,
                                    get_url_checks,
                                    get_url_check_last,
                                   )
from page_analyzer.validators import validate_url, is_null
from page_analyzer.logic_checks import check_response

load_dotenv()

app = Flask(__name__)
SECRET_KEY = os.getenv('SECRET_KEY')
app.secret_key = SECRET_KEY


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/urls')
def urls():
    messages = get_flashed_messages(with_categories=True)
    data = get_urls()
    for item in data:
        data_check = get_url_check_last(item['id'])
        if data_check is None:
            item['last_check'] = ''
            item['status_code'] = ''
        else:
            item['last_check'] = data_check['created_at'].date()
            item['status_code'] = data_check['status_code']
    return render_template('urls.html', data=data, messages=messages)


@app.post('/urls')
def url_add():
    data = {}
    url = request.form.get('url')
    errors = validate_url(url)
    if 'not valid' in errors['status']:
        if 'exists' in errors['status']:
            flash('Страница уже существует', 'warning')
            return redirect(url_for('get_url_id', id=errors['url']['id']))
        flash('Некорректный URL', 'error')
        if 'exceeded size' in errors['status']:
            flash('URL превышает 255', 'error')
        elif 'zero size' in errors['status']:
            flash('URL обязателен', 'error')
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html', messages=messages), 422

    data['url'] = url
    data['created_at'] = datetime.datetime.now().date()
    create_url(data)
    data = get_id_url_by_name(url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_url_id', id=data['id']))


@app.get('/urls/<id>')
def get_url_id(id):
    messages = get_flashed_messages(with_categories=True)
    data = get_url_by_id(int(id))
    if is_null(data):
        return render_template('index.html'), 404
    data_checks = get_url_checks(int(id))
    return render_template('url_id.html', data=data,
                           data_checks=data_checks,
                           messages=messages)


@app.post('/urls/<id>/checks')
def check_url(id):
    data = {}
    data["url_id"] = int(id)
    data["created_at"] = datetime.datetime.now().date()
    url = get_name_url_by_id(int(id))

    info_check = check_response(url["name"])
    if info_check["error"]:
        flash('Произошла ошибка при проверке', 'error')
    else:
        data.update(info_check)
        create_check(data)
        flash('Страница успешно проверена', 'success')
        
    return redirect(url_for('get_url_id', id=data["url_id"]))
