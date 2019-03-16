from peewee import *
from flask_login import UserMixin

db = SqliteDatabase(None)

class BaseModel(Model):
    class Meta:
        database = db
        order_by = ('-desc', )

class Writer(UserMixin, BaseModel):
    username = CharField()
    password = CharField()
    email = CharField()

def initialize_db():
    db.connect(reuse_if_open=True)
    db.create_tables([Writer])
    db.close()
    

