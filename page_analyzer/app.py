import os
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
                                    get_url_by_name
                                   )
from page_analyzer.validators import validate_url, is_null

load_dotenv()

app = Flask(__name__)
SECRET_KEY = os.getenv('SECRET_KEY')
app.secret_key = SECRET_KEY


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/urls')
def urls():
    messages = get_flashed_messages(with_categories=True)
    data = get_urls()
    return render_template('urls.html', data=data, messages=messages)


@app.post('/urls')
def url_add():
    data = {}
    url = request.form.get('url')
    errors = validate_url(url)
    if 'not valid' in errors['status']:
        flash('Некорректный URL', 'error')
        if 'exists' in errors['status']:
            flash('Страница уже существует', 'warning')
            return redirect(url_for('get_url_id', id=errors['url'][0]))
        if 'exceeded size' in errors['status']:
            flash('URL превышает 255', 'error')
        elif 'zero size' in errors['status']:
            flash('URL обязателен', 'error')
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html', messages=messages), 422

    data['url'] = url
    data['date'] = datetime.datetime.now()
    create_url(data)
    data = get_url_by_name(url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_url_id', id=data[0]))


@app.get('/urls/<id>')
def get_url_id(id):
    messages = get_flashed_messages(with_categories=True)
    data = get_url_by_id(id)
    if is_null(data):
        return render_template('index.html'), 404
    return render_template('url_id.html', data=data, messages=messages)
