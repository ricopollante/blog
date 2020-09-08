# Router / Views
Installation setup:
create db name(postgresql) : apidb
postgresql user: postgres
postgresql password: root


cd blog

pipenv install psycopg2 flask-migrate flask-script marshmallow flask-bcrypt pyjwt flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy requests

pipenv -m shell
flask db init
flask db migrate
flask db upgrade
python app.py

USERS:

-Get All members

curl -i -H "Content-Type: application/json" -X GET 127.0.0.1:5000/members



-Member signup / First to signup is the admin
I used userid the determined the admin and a normal user,
so basically admin userid is 1 and normal user will be > 1.

curl -i -H "Content-Type: application/json" -X POST -d "{\"username\":\"root\", \"password\":\"admin\"}" 127.0.0.1:5000/member/signup



LOGIN Authentication / web tokens /

curl -i -H "Content-Type: application/json" -X POST -d "{\"password\":\"pass\",\"username\":\"admin\"}" 127.0.0.1:5000/login

Output: 
{
    Token: as6dgvyyrg77rjjjoe98u;
}

List:

-Get categories

#curl -i -H "Content-Type: application/json" -X GET 127.0.0.1:5000/categories




-Add category

If token was correct it will return "Status : OK" 
and new Category will be added to database.
If not it will "Error: Token Invalid
and you cant add new category.

I used JWT to check if token was admin or a normal member .

#curl -i -H "Content-Type: application/json" -X POST -d "{\"title\":\"World News\"}" 127.0.0.1:5000/category/add?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoicm9vdCIsImV4cCI6MTU5OTUyNTE0MX0.ss7lbx_4KwWUszNw03CvlZ38o-n3hGNjtl_QXGh7ZlM




Cards:

-Create CARDS / NEWS

curl -i -H "Content-Type: application/json" -X POST -d "{\"title\":\"news 4\", \"description\":\"this is a News 4\", \"owner_id\":\"1\", \"category_id\":\"1\"}" 127.0.0.1:5000/news/add?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoicm9vdCIsImV4cCI6MTU5OTUyNTE0MX0.ss7lbx_4KwWUszNw03CvlZ38o-n3hGNjtl_QXGh7ZlM

If token was correct it will 
add new News to database.
If not it will "Error: Token Invalid
and you cant add new News.

I used JWT token to get ID of a user to determine the who's added new news.


-Get All News

curl -i -H "Content-Type: application/json" -X GET 127.0.0.1:5000/news




-Get Single News

curl -i -H "Content-Type: application/json" -X GET 127.0.0.1:5000/news/1


-Update News

curl -i -H "Content-Type: application/json" -X PUT -d "{\"name\":\"News 4\", \"description\":\"this is a News 4\", \"price\":\"50.00\",\"qty\":\"300\"}" 127.0.0.1:5000/News


-Get Delete News

curl -i -H "Content-Type: application/json" -X DELETE 127.0.0.1:5000/News/1

PS: due to a limited amount of time to build this api, I cant organize the Structure / Unit testing of my app pretty well , so I used my time mainly for the Routers/Views and documentations. 
