from alayatodo import app
from wtforms.validators import DataRequired
from sqlalchemy import desc 
from wtforms import Form, TextField
from .models import Users, Todos 
from alayatodo import app, db 
from config import TODOS_PER_PAGE
from flask import (
    g,
    redirect,
    render_template,
    request,
    session, 
    flash,
    jsonify
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
    # querying db with sqlalchemy
    user = Users.query.filter_by(username=username, password=password).first()
    if user:
        id_user =  dict((col, getattr(user, col)) for col in user.__table__.columns.keys())
        session['user'] = id_user 
        session['logged_in'] = True
        return redirect('/list_todos')

    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    # querying db with sqlalchemy
    todo = Todos.query.filter_by(id=id).first()
    return render_template('todo.html', todo=todo)


#edit home route path, to avoid miss confusion with the above /todo/id link
@app.route('/list_todos', methods=['GET'])
@app.route('/list_todos/<int:page>', methods=['GET'])
def todos(page=1):
    if not session.get('logged_in'):
        return redirect('/login')
    # querying db with sqlalchemy
    todos = Todos.query.order_by(desc(Todos.id)).paginate(page, TODOS_PER_PAGE, error_out=False)
    return render_template('todos.html', todos=todos)
    

@app.route('/list_todos', methods=['POST'])
@app.route('/list_todos/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')

    # we pass a form object to check the content
    description = DescriptionForm(request.form)

    if description.validate():
        # if the content is valide
        # we assign the content of the field in this variable 
        description_text = request.form.get('description')
        todo=Todos(description=description_text, user_id=session['user']['id'])
        db.session.add(todo)
        db.session.commit()
        
        return redirect('/list_todos')
    else:
        flash('The description field is required.','warning')

    return redirect('/list_todos')


@app.route('/todo/<id>/json', methods=['GET'])
def todos_json(id):
    if not session.get('logged_in'):
        return redirect('/login')
    todo = Todos.query.filter_by(id=id).first()
    todo_json =  dict((col, getattr(todo, col)) for col in todo.__table__.columns.keys())
    return jsonify(todo_json)


@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    
    todo = Todos.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect('/list_todos')


@app.route('/todocompleted/<id>', methods=['POST'])
def todo_completed(id):
    if not session.get('logged_in'):
        return redirect('/login')
    todo = Todos.query.filter_by(id=id).update({'is_completed':True})
    #todo.is_completed = True
    db.session.commit()
    return redirect('/list_todos')
