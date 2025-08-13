from flask import Flask, request 
from flask import render_template
from jinja2 import Template
from markupsafe import escape
import json
import uuid
from flask import Flask, redirect, render_template, request, url_for, flash, get_flashed_messages


users = json.load(open('users.json', 'r'))
app = Flask(__name__)

app.secret_key = "secret_key"

# users = [
#     {"id": 1, "name": "mike"},
#     {"id": 2, "name": "mishel"},
#     {"id": 3, "name": "adel"},
#     {"id": 4, "name": "keks"},
#     {"id": 5, "name": "kamila"},
# ]

@app.get("/")
def index():
    app.logger.info("Получен запрос к главной стрнице")
    return "Hello, World!"

# @app.get("/users/")
# def users_get():
#     return "Ответ от GET /users"

# @app.get("/users/")
# def users_get():
#     users = [
#         {"id": 1, "name": "mike"},
#         {"id": 2, "name": "mishel"},
#         {"id": 3, "name": "adel"},
#         {"id": 4, "name": "keks"},
#         {"id": 5, "name": "kamila"},
#     ]
#     query = request.args.get('query').lower()
#     if query:
#         users = [
#             user for user in users if query in user['name'].lower()
#         ]
#     else:
#         users=users
#     return render_template(
#         'users.html',
#         users=users,
#         search=query,
#     )

@app.get("/users/")
def users_get():
    messages = get_flashed_messages(with_categories=True)
    app.logger.info("Получен запрос к /users/")
    with open('users.json', 'r') as f:
        users = json.load(f)
    term = request.args.get('term', '')
    term = term.lower()
    filtered_users = [user for user in users if term in user['name'].lower()]

    return render_template(
        'users.html',
        users=filtered_users,
        search=term,
        messages=messages,
    )


@app.post("/users/")
def users_post():
    user_data = request.form.to_dict()
    errors = validate(user_data)
    if errors:
        return render_template(
            'new.html',
            user=user_data,
            errors=errors,

        )
    id = str(uuid.uuid4())
    user = {
        "id": id,
        "name": user_data['name'],
        "email": user_data['email'],
    }
    users.append(user)
    with open('./users.json', 'w') as f:
        json.dump(users, f)
    flash("Hello, Nikita!", "success")
    return redirect(url_for('users_get', code=302))


#Внизу тестовая функция
@app.post("/users/flash-test/")
def users_flash_test():
    flash("Hello, Nikita!", "success")
    return redirect(url_for("get_hello"))
# @app.post("/users")
# def users_post():
#     return 'Users', 302

@app.route('/users/new')
def users_new():
    user = {'name': '', 'email': ''}
    errors = {}
    return render_template(
        'new.html',
        user=user,
        errors=errors,
    )

#внизу тестовая функция
@app.get('/users/new')
def get_hello():
    messages = get_flashed_messages(with_categories=True)
    print(messages)
    return render_template(
        'bar.html',
        messages=messages,
    )
    

@app.route('/courses/<id>')
def get_course(id):
    return f"Курс с id {id}"

@app.route('/users/<id>')
def show_user(id):
    user = {
        "id": id,
        "name": f"user-{id}"
    }
    return render_template(
        'index.html',
        user=user,
    )

@app.route('/users/<string:nickname>/<int:id>')
def users_show(nickname, id):
    return render_template(
        "show2.html",
        nickname=nickname,
        id=id,
    )

@app.route('/nikita')
def user_nikita():
    return render_template("/courses/index.html")

@app.route('/courses/')
def courses():
    courses = [
        {"id": 1, "title": "Python"},
    ]
    return render_template("/courses/index.html", courses=courses)

subs = ['math', 'physics', 'chemistry']



# cities = [
#     {'id': 1, 'city': 'Москва'},
#     {'id': 2, 'city': 'Санкт-Петербург'},
#     {'id': 3, 'city': 'Новосибирск'},
#     {'id': 5, 'city': 'Красноярск'},
#     {'id': 7, 'city': 'Екатеринбург'},
# ]

# cars = [
#     {'model': 'BMW', 'price': 100000},
#     {'model': 'Audi', 'price': 150000},
#     {'model': 'Ford', 'price': 120000},
#     {'model': 'Mercedes', 'price': 200000}
# ]

# link = '''
# <select name="cities">
# {% for c in cities -%}
# {% if c['id'] > 6 -%}
# <option value="{{c['id']}}">{{c['city']}}</option>
# {% elif c['city'] == 'Москва' -%}
# <option>{{c['city']}} сработало?</option>
# {% else -%}
# {{c['city']}}
# {% endif -%}
# {% endfor -%}
# </select>
# '''
# persons = [
#     {'name': 'Иван', 'age': 20, 'weight': 70},
#     {'name': 'Петр', 'age': 30, 'weight': 80},
#     {'name': 'Nikita', 'age': 31, 'weight': 67}
# ]

# html = '''
# {% macro list_users(list_of_users) -%}
# <ul>
# {% for u in list_of_users -%}
# <li>{{u.name}} {{caller(u)}}
# {% endfor -%}
# </ul>
# {% endmacro %}

# {% call(user) list_users(users) -%}
# <ul>
# <li>age:{{user.age}}
# <li>weight:{{user.weight}}
# </ul>
# {% endcall %}
# '''

subs2 = '''
{% for l in list_tables %}
<ul>
<li>{{l}}</li>
{% endfor %}
</ul>'''

tm = Template(subs2)
msg = tm.render(list_tables=subs)

print(msg)

def validate(user):
    errors = {}
    if not user['name']:
        errors['name'] = "Can't be blank"
    if not user['email']:
        errors['email'] = "Can't be blank"
    return errors