from flask import Flask, render_template, request, flash,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, UserMixin, logout_user
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SECRET_KEY'] = 'this is secret'
db = SQLAlchemy(app)

login_manger=LoginManager()
login_manger.init_app(app)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    fname = db.Column(db.String(120), nullable=False)
    lname = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    def __repr__(self):
        return "<User %r>" % self.username

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80),nullable=False)
    content = db.Column(db.Text(),nullable=False)  
    pub_date = db.Column(db.DateTime(),nullable=False,default=datetime.utcnow)
    author = db.Column(db.String(20),nullable=False,default='N/A')
    def __repr__(self):
        return "Blog %r>" % self.title

@login_manger.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 


@app.route("/")
def index():
    return render_template("index.html")       
@app.route("/main")
def main():
    return render_template("main.html")

@app.route("/register",methods=['GET','POST'])
def register():
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('uname')
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        user = User(username=username,email=email,fname=fname,lname=lname,password=password)
        db.session.add(user)
        db.session.commit()
        flash('user has been registered successfully','success')
        return redirect('/login')

    return render_template("register.html")

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
       username = request.form.get('username')
       password = request.form.get('password')

       user = User.query.filter_by(username=username).first()
       if user and password==user.password:
           login_user(user)
           return redirect('/')
       else:
           flash('Invaild Credentials', 'danger')
           return redirect('/login')


    return render_template("login.html")

@app.route("/logout")
def logout():
    login_user() 
    return redirect('/')

@app.route("/blogpost")
def blogpost():
    return render_template('/blog.html')



if __name__== "__main__":
    app.run(debug=True)