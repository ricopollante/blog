from flask import Flask

app = Flask(__name__)

#DatabaseConnection / Config
app.config['SQLALCHEMY_DATABASE_URI']='postgres://postgres:root@localhost:5432/apidb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "dummysecretkey"
