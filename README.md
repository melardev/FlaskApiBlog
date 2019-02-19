# Introduction
Flask Blog api app, this application is **not finished**. 
# Getting started
1. Git clone
2. execute reset.bat to make migrations, migrate
3. Seed the database with: python2 seed_db
4. Run server with python2.py app.py

# Features implemented
- Seeding All models: Article, Comment, Like, UserSubscription, User, Role, Tag, Category
- Controller Articles
- Controller Comment
- Authentication/Authorization
- Follower/Following authors
- Middlewares: Benchmark + User loader

# useful commands

flask2 db init
flask2 db migrate -m 'initial migration'
flask2 db upgrade

# TODO
- I am trying to migrate from using the classic blueprint to use Flask-RestFul
# Resources
- [Flask JWT](https://pythonhosted.org/Flask-JWT/)
- [Flask Config](http://flask.pocoo.org/docs/0.12/config/#config)