from binascii import Incomplete
from urllib import request
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

""" COMENTAR VARIAS LINEA ALT  + SHIFT + A """

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    complete = db.Column(db.Boolean)

#Borrar la base de datos, se recorre y se bora una a una
for i in Todo.query.all(): 
    todo = Todo.query.filter_by(id=i.id).first()
    db.session.delete(todo)
    db.session.commit()

@app.route('/')
def index():
    incomplete = Todo.query.filter_by(complete=False).all()
    complete = Todo.query.filter_by(complete=True).all()
    return render_template('index.html', incomplete=incomplete, complete= complete)

@app.route('/add', methods=['POST'])
def add():
    print(request.form['todoitem'])
    todo = Todo(text=request.form['todoitem'], complete =False)
    db.session.add(todo)
    db.session.commit()
    print(todo.text)
    print(todo.id)
    print(todo.complete)
    return redirect(url_for('index'))    

@app.route('/complete/<id>')
def complete(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    print(todo)
    todo.complete = True
    db.session.commit()
    print(todo.complete)
    return redirect(url_for('index'))  

@app.route('/uncheck/<id>')
def uncheck(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete=False
    db.session.commit()
    return redirect(url_for('index'))  

@app.route('/delete/<id>')
def delete(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index')) 

if __name__ == '__main__':
    app.run(debug=True)
