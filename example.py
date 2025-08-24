from flask import Flask, request 
from flask import render_template
from jinja2 import Template
from markupsafe import escape
import json
import uuid
from flask import Flask, redirect, render_template, request, url_for, flash, get_flashed_messages
from dotenv import load_dotenv
import os 

app = Flask(__name__)

load_dotenv()

# users = json.load(open('users.json', 'r'))
# app = Flask(__name__)
# app.config.from_pyfile('config.py')

# app.secret_key = "secret_key"

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["DEBUG"] = os.getenv("DEBUG", "False") == "True"
app.config["DATABASE_URL"] = os.getenv("DATABASE_URL")

@app.get("/")
def index():
    app.logger.info("Получен запрос к главной стрнице")
    return "Hello, World!"

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

@app.route('/users/<id>', endpoint='show2')
def users_show(id):
    user = {
        "id": id,
        "name": f"user-{id}"
    }
    return render_template(
        'index.html',
        user=user,
    )

@app.route('/users/<string:nickname>/<int:id>', endpoint='show')
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

if __name__ == "__main__":
    app.run(debug=True, port=8000)
