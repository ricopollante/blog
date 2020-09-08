from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
import jwt
import datetime
from config import app


#Init db
db = SQLAlchemy(app)
#init MA/Serializer
ma = Marshmallow(app)
#migrate models
migrate = Migrate(app, db)



#commit DB
db.create_all()

#Models
class Member(db.Model):
    __tablename__= "member"
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), unique=True)
    member_news = db.relationship('News', backref='member')
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
        
class Category (db.Model):
    __tablename__: "category"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    news_list = member_news = db.relationship('News', backref='category')
    
    def __init__(self, title):
        self.title = title



class News(db.Model):
    __tablename__= "news"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    owner_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    news_comments = db.relationship('Comments', backref='news')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __init__(self, title, description, owner_id, category_id):
        self.title = title
        self.description = description
        self.owner_id = owner_id
        self.category_id = category_id
        

class Comments(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(2000))
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'))

    def __init__(self, message, news_id):
        self.message = message
        self.news_id = news_id







#News / Schema / Serializer
class NewsSchema(ma.Schema):
    class Meta:
        fields = ('id','title','description', 'owner_id','category_id')
    
class NewsAllSchema(ma.Schema):
    class Meta:
        fields = ('id','title','description','owner_id','category_id')

class MemberSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password')

class MembersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password')

class CommentsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'message', 'news_id')

class CategorySchema (ma.Schema):
    class Meta:
        fields = ('id','title')

class CategoriesSchema (ma.Schema):
    class Meta:
        fields = ('id','title')
    
# Init Schema
news_schema = NewsSchema()
newsall_schema = NewsAllSchema(many=True)
member_schema = MemberSchema()
members_schema = MembersSchema(many=True)
comments_schema = CommentsSchema()
category_schema = CategorySchema()
categories_schema = CategoriesSchema(many=True)



# Router / Views

#New news category
#curl -i -H "Content-Type: application/json" -X POST -d "{\"title\":\"World News\"}" 127.0.0.1:5000/category/add?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoicm9vdCIsImV4cCI6MTU5OTUyNTE0MX0.ss7lbx_4KwWUszNw03CvlZ38o-n3hGNjtl_QXGh7ZlM
"""
If token was correct it will return "Status : OK" 
and new Category will be added to database.
If not it will "Error: Token Invalid
and you cant add new category.

I used JWT to check if token was admin or a normal member .
"""

@app.route('/category/add', methods=['POST'])
def add_category():
    token = request.args.get('token')
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'])
    except Exception:
        return jsonify({"Error" : "Token Invalid "})

    if data:
        uid = data['user']
        userid = Member.query.filter_by(username = uid).first()
        
        if userid.id == 1:
            title = request.json['title']
            new_category = Category(title)
            db.session.add(new_category)
            try:
                db.session.commit()
            except Exception:
                pass
        return jsonify({"status" : "OK"})

    else:
        return jsonify({"Error" : "Token Invalid "})

    

#Get categories
#curl -i -H "Content-Type: application/json" -X GET 127.0.0.1:5000/categories
@app.route('/categories', methods=['GET'])
def get_categories():
    all_news = Category.query.all()
    result = categories_schema.dump(all_news)
    return jsonify(result)



# Add COMMENTS
#curl -i -H "Content-Type: application/json" -X POST -d "{\"message\":\"So many dead already\",\"news_id\":\"1\"}" 127.0.0.1:5000/comment/add
@app.route('/comment/add', methods=['POST'])
def add_comment():
    message = request.json['message']
    news_id = request.json['news_id']


    new_comment = Comments(message, news_id)

    db.session.add(new_comment)
    db.session.commit()

    return comments_schema.jsonify(new_comment)


# Create News / CARDS
#curl -i -H "Content-Type: application/json" -X POST -d "{\"title\":\"news 4\", \"description\":\"this is a News 4\", \"owner_id\":\"1\", \"category_id\":\"1\"}" 127.0.0.1:5000/news/add?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoicm9vdCIsImV4cCI6MTU5OTUyNTE0MX0.ss7lbx_4KwWUszNw03CvlZ38o-n3hGNjtl_QXGh7ZlM
"""
If token was correct it will 
add new News to database.
If not it will "Error: Token Invalid
and you cant add new News.

I used JWT token to get ID of a user to determine the who's added new news.
"""
@app.route('/news/add', methods=['POST'])
def add_news():
    token = request.args.get('token')
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'])
    except Exception:
        return jsonify({"Error" : "Token Invalid "})


    if data:
        uid = data['user']
        userid = Member.query.filter_by(username = uid).first()
        title = request.json['title']
        description = request.json['description']
        owner_id = userid.id
        category_id = request.json['category_id']


    

    new_news = News(title, description, owner_id, category_id)

    db.session.add(new_news)
    db.session.commit()

    return news_schema.jsonify(new_news)

#Get All News
#curl -i -H "Content-Type: application/json" -X GET 127.0.0.1:5000/news
@app.route('/news', methods=['GET'])
def get_news():
    all_news = News.query.all()
    result = newsall_schema.dump(all_news)
    return jsonify(result)

#Get Single News
#curl -i -H "Content-Type: application/json" -X GET 127.0.0.1:5000/news/1
@app.route('/news/<id>', methods=['GET'])
def get_news_single(id):
    news = News.query.get(id)
    result =  news_schema.dump(news)
    return jsonify(result)

#Update News
#curl -i -H "Content-Type: application/json" -X PUT -d "{\"name\":\"News 4\", \"description\":\"this is a News 4\", \"price\":\"50.00\",\"qty\":\"300\"}" 127.0.0.1:5000/News
@app.route('/news/<id>', methods=['PUT'])
def update_news(id):
    news = News.query.get(id)
    title = request.json['title']
    description = request.json['description']
    owner_id = request.json['owner_id']

    news.title = title
    news.description = description
    news.owner_id = owner_id

    db.session.commit()
    return news_schema.jsonify(news)

#Get Delete News
#curl -i -H "Content-Type: application/json" -X DELETE 127.0.0.1:5000/News/1
@app.route('/news/<id>', methods=['DELETE'])
def delete_news(id):
    news = News.query.get(id)
    db.session.delete(news)
    db.session.commit()

    return news_schema.jsonify(news)

#Member/ USERS / router / Views
#member signup
#curl -i -H "Content-Type: application/json" -X POST -d "{\"username\":\"root\", \"password\":\"admin\"}" 127.0.0.1:5000/member/signup
@app.route('/member/signup', methods=['POST'])
def add_member():
    username = request.json['username']
    password = request.json['password']

    new_member = Member(username, password)

    db.session.add(new_member)
    db.session.commit()

    return member_schema.jsonify(new_member)

 
#Get All members
#curl -i -H "Content-Type: application/json" -X GET 127.0.0.1:5000/members
@app.route('/members', methods=['GET'])
def get_members():
    all_news = Member.query.all()
    result = members_schema.dump(all_news)
    return jsonify(result)   


#Authentication / web tokens / GET TOKEN
#curl -i -H "Content-Type: application/json" -X POST -d "{\"password\":\"pass\",\"username\":\"admin\"}" 127.0.0.1:5000/login
@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    userpassword = Member.query.filter_by(username=username).first()
    userid = Member.query.filter_by(username=username).first()
    try:
        if password == userpassword.password :
            token = jwt.encode({'user' : username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

            return jsonify({"token" : token.decode('UTF-8')})
    except Exception as error:
        return jsonify({"error" : "Login error. Please try again."})



if __name__== '__main__':
    app.run(debug=True)
