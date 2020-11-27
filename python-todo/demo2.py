from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'super secret key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///demo2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)


# create a database

class TODOS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))

    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return '<Task %r>' % self.id


class TosdoSchema(ma.Schema):
    class Meta:
        field = "content"


todo_schema = TosdoSchema()
todos_schema = TosdoSchema(many=True)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        content = request.form['content']
        print(content)
        # if task_content == "":
        # flash('the content field ivalid')
        new_task = TODOS(content)
        print(new_task)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = TODOS.query.all()
        # tasks = todos_schema.dump(tasksall)

        return render_template('demo2_index.html', tasks=tasks)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    datas = TODOS.query.get_or_404(id)

    if request.method == 'POST':
        datas.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=datas)


@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    task = TODOS.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/')
    '''
    task_to_delete = TODOS.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'
    '''


if __name__ == "__main__":
    app.run(port=3002, debug=True)
