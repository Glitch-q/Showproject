from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'

db = SQLAlchemy(app)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)
    cat = db.Column(db.String(20))

@app.route('/')
def index():
    posts = Project.query.order_by(Project.date_posted.desc()).all()

    return render_template('index.html', posts=posts)

@app.route('/admin')
def admin():
    posts = Project.query.order_by(Project.date_posted.desc()).all()

    return render_template("admin_index.html", posts=posts)

@app.route('/search')
def search():
    return render_template("search.html")

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Project.query.filter_by(id=post_id).one()

    return render_template('post.html', post=post)

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/addpost', methods=['POST'])
def addpost():
    title = request.form['title']
    author = request.form['author']
    content = request.form['content']
    cat = request.form['cat']

    post = Project(title=title, author=author, content=content, cat=cat, date_posted=datetime.now())

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))

@app.route("/delete/<int:post_id>")
def delete(post_id):
    post = Project.query.filter_by(id=post_id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)