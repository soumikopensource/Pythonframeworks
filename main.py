from flask import Flask,render_template,request
#for datbase
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json  # to read config.json
#make an app

with open('config.json','r') as file:
    params=json.load(file)['params']
local_server=True

app=Flask(__name__)
app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT='465',
    MAIL_USE_SSL='True',
    MAIL_USERNAME=params['gmail_user'],
    MAIL_PASSWORD=params['gmail_passwd']
)
mail=Mail(app)

#database connect with sql
if local_server:
    app.config['SQLALCHEMY_DATABASE_URI']=params['local_url']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_url']

db = SQLAlchemy(app)

#make your own tables
#contacts
class Contacts(db.Model):
    sl= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(50), unique=True,nullable=False)
    content= db.Column(db.String(120), unique=False, nullable=False)


class Posts(db.Model):
    sl = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    slug = db.Column(db.String(80), unique=False, nullable=False)
    content = db.Column(db.String(80), unique=False, nullable=False)
    date= db.Column(db.String(12), unique=False, nullable=False)
    img_file= db.Column(db.String(20), unique=False, nullable=False)



@app.route("/")
def index():

    return render_template('index.html',params=params)
#about route endpoint

@app.route("/about")
def about():
    return render_template('about.html',params=params)



@app.route("/contact",methods=['GET','POST'])
def contact():
    if request.method=='POST':
        #fetch  to database
        name=request.form.get('name')
        email = request.form.get('email')
        phone_num = request.form.get('phone')
        message = request.form.get('message')
        #add entries to database
        entry=Contacts(name=name,email=email,phone=phone_num,content=message)
        db.session.add(entry)
        db.session.commit()
        mail.send_message("new message from your site",
                          sender=email,
                          recipients=[params['gmail_user']],
                          body=message)




    #first name is from template ,second from python
    return render_template('contact.html',params=params) # accessed from html file

@app.route("/post/<string:post_slug>",methods=['GET'])
def post_route(post_slug):

    post=Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html',params=params,post=post) # accessed from html file

app.run(debug=True)