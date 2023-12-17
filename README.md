# flaskintro
```
init database as follows

start python
>>> from app import app,db
>>> app.app_context().push()
>>> db.create_all()
>>> exit ()

database file in ./instance
```