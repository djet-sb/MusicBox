from playhouse.postgres_ext import *
import datetime, json

user = 'postgres'
password = 'Pasd@1234'
db_name = 'musicbox'

db = PostgresqlDatabase(
    db_name, user=user,
    password=password,
    host='localhost'
)


class musicbox(Model):
    publish_in = DateField()
    published_in = DateField()
    publish_data = JSONField()
    class Meta:
        database = db  # This model uses the "people.db" database.

musicbox.create_table(True)
musicbox.create(publish_in=datetime.date(2019, 3, 22),
                publish_data=str({"test":"1223"}))