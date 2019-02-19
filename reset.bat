rm -r migrations
rm app.db
flask2 db init && flask2 db migrate -m 'initial' && flask2 db upgrade