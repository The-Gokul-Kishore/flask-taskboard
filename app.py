from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(200),nullable=False)
    completed = db.Column(db.Integer,default=0)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    def __repr__(self):
        return '<Task %r>' % self.id
    

@app.route('/',methods =['POST','GET'] )
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content = task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an issue in task adding'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        
        return render_template('index.html',tasks=tasks)
@app.route('/delete/<int:id>')
def delete(id):
    task_tot_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_tot_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "there was an issue in the deleting the requested item"
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)

    if(request.method=='POST'):
        task_to_update.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "there was issue updating your task"
    else:
        return render_template('update.html',task=task_to_update)
    try:
        print('nothing for now')
    except:
        return "error here"
if __name__=="__main__":
    app.run(debug=True)