import config
from playhouse.postgres_ext import *

user = config.DATABASE.user
password = config.DATABASE.password
db_name = config.DATABASE.db_name
host = config.DATABASE.host
db = PostgresqlDatabase(
    db_name, user=user,
    password=password,
    host=host
)


class Publications(Model):
    channel_id = IntegerField()
    publish_in = IntegerField()
    published_in = IntegerField(default=0)
    publish_data = JSONField()

    class Meta:
        database = db  # This model uses the "people.db" database.


class Channels(Model):
    channel_name = TextField()
    chat_id = FloatField()
    token = TextField()

    class Meta:
        database = db  # This model uses the "people.db" database.


try:
    Channels.create_table(True)
    Publications.create_table(True)
except OperationalError as err:
    print(err)
    exit(1)

