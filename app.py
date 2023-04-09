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

@app.route('/prc')
def template_inheritance():
    return render_template('prc.html')
@app.route('/')
def hello_world():
    return 'Hello, World!'
@app.route('/template', methods =['GET','POST'])
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
    return redirect('/template')
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
        return redirect('/template')    
    updatelist = Mylist.query.filter_by(sno = sno).first()
    return render_template('update.html',update_list = updatelist)
# @app.route('/page2')
# def sec_page():
#     fulllist = Mylist.query.all()
#     return f'Data: {fulllist}'

if __name__ == "__main__":
    app.run(debug = True, port= 8000)


# =========================================================
# from flask import Flask, request, render_template
# import requests
# from bs4 import BeautifulSoup

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('prc.html')

# @app.route('/', methods=['POST'])
# def compare_websites():
#     url1 = request.form['url1']
#     url2 = request.form['url2']

#     # Get the HTML content of the two websites
#     page1 = requests.get(url1)
#     page2 = requests.get(url2)

#     # Compare the length of the HTML contents
#     if len(page1.content) > len(page2.content):
#         largest_content = page1.content
#     else:
#         largest_content = page2.content

#     # Parse the HTML of the larger website and find the center main content
#     soup = BeautifulSoup(largest_content, 'html.parser')
#     center_content = soup.find('main', {'class': 'center'})

#     # If no center content is found, look for a div with a class of 'center'
#     if not center_content:
#         center_content = soup.find('div', {'class': 'center'})

#     # If still no center content is found, use the body tag as the center content
#     if not center_content:
#         center_content = soup.body

#     # Render the result template with the center content of the larger website
#     return render_template('result.html', center_content=str(center_content))

# if __name__ == '__main__':
#     app.run(debug=True)

# ====================================================

