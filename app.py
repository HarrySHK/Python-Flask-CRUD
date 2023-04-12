from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///harry.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Mylist(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    topic = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(200), nullable = False)
    date_time = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f'{self.sno} - {self.topic} - {self.desc} - {self.date_time}'

@app.route('/', methods =['GET','POST'])
def temp():
    if request.method == 'POST':
        topic = request.form['topic']
        desc = request.form['desc']
        mylist = Mylist(topic = topic, desc = desc)
        db.session.add(mylist)
        db.session.commit()
    fulllist = Mylist.query.all()
    return render_template('index.html', alllist = fulllist)
@app.route('/delete/<int:sno>')
def delete(sno):
    fulllist = Mylist.query.filter_by(sno = sno).first()
    db.session.delete(fulllist)
    db.session.commit()
    return redirect('/')
@app.route('/update/<int:sno>', methods = ['GET','POST'])
def update(sno):
    if request.method == 'POST':
        topic = request.form['topic']
        desc = request.form['desc']
        updatelist = Mylist.query.filter_by(sno = sno).first()
        updatelist.topic = topic
        updatelist.desc = desc
        db.session.add(updatelist)
        db.session.commit()
        return redirect('/')    
    updatelist = Mylist.query.filter_by(sno = sno).first()
    return render_template('update.html',update_list = updatelist)

if __name__ == "__main__":
    app.run(debug = True, port= 8000)

