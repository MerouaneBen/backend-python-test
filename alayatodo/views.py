from alayatodo import app
from wtforms.validators import DataRequired  
from wtforms import Form, TextField
from .models import Users, Todos 
from alayatodo import app, db 
from flask import (
    g,
    redirect,
    render_template,
    request,
    session, 
    flash
    )


class DescriptionForm(Form):
    """this class validate the content of the description filed.
    this field must not be empty, and also no blank spaces.
    """
    description = TextField('Description', validators=[DataRequired()])

@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l.decode('utf-8') for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')

    user = Users.query.filter_by(username=username, password=password).first()
    #sql = "SELECT * FROM users WHERE username = '%s' AND password = '%s'";
    #cur = g.db.execute(sql % (username, password))
    #user = cur.fetchone()
    if user:
        session['user'] = username
        session['logged_in'] = True
        return redirect('/todo')

    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    cur = g.db.execute("SELECT * FROM todos WHERE id ='%s'" % id)
    todo = cur.fetchone()
    return render_template('todo.html', todo=todo)


@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
def todos():
    if not session.get('logged_in'):
        return redirect('/login')
    #cur = g.db.execute("SELECT * FROM todos")
    #todos = cur.fetchall()
    todos = Todos.query.all()
    return render_template('todos.html', todos=todos)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')

    # we pass a form object to check the content
    description = DescriptionForm(request.form)

    if description.validate():
        # if the content is valide
        # we assign the content of the field in this variable 
        description_text = request.form.get('description')
        g.db.execute(
            "INSERT INTO todos (user_id, description) VALUES ('%s', '%s')"
            % (session['user']['id'], description_text) # request.form.get('description', '') I'm not sure about why we have 2 elements iside this tuple, when we need only one value.
        )
        g.db.commit()
        return redirect('/todo')
    else:
        flash('The description field is required. ')

    return redirect('/todo')

@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    g.db.execute("DELETE FROM todos WHERE id ='%s'" % id)
    g.db.commit()
    return redirect('/todo')
