from peewee import *
from playhouse.migrate import * 
from flask_login import UserMixin

db = SqliteDatabase(None)

class BaseModel(Model):
    class Meta:
        database = db
        order_by = ('-desc', )

class Writer(UserMixin, BaseModel):
    first_name = CharField()
    last_name = CharField()
    username = CharField(primary_key=True)
    password = CharField()
    email = CharField(unique=True)

def initialize_db():
    db.connect(reuse_if_open=True)
    db.create_tables([Writer])
    db.close()
    