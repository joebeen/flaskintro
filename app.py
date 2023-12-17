from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)
# db.get_engine(app).execute("CREATE TABLE IF NOT EXISTS todo (id INTEGER PRIMARY KEY, content TEXT, data_created DATETIME, completed INTEGER DEFAULT 0)")

class Todo (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    priority = db.Column(db.Integer, default=3)
    completed = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return '<Task %r>' % self.id
    

@app.route('/', methods=['POST', 'GET']) 
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        task_priority = request.form['priority']
        new_task = Todo (content=task_content, priority=task_priority)
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
        
    else:
        tasks = Todo.query.order_by(Todo.priority).all()
        return render_template('index.html', tasks=tasks)
    
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    
    if request.method == 'POST':
        task.content = request.form['content']
        task.priority = request.form['priority']
                
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)
    

if __name__ == '__main__':
    app.run(debug=True)

