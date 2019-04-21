from playhouse.postgres_ext import *
import datetime

user = 'postgres'
password = 'Pasd@1234'
db_name = 'musicbox'

db = PostgresqlDatabase(
    db_name, user=user,
    password=password,
    host='localhost'
)


class musicbox(Model):
    publish_in = IntegerField()
    published_in = IntegerField(default=0)
    publish_data = JSONField()

    class Meta:
        database = db  # This model uses the "people.db" database.


publish_in_unixtime = int(datetime.datetime(2010, 2, 25, 23, 23).timetuple())

# Over
# datetime.datetime.utcfromtimestamp(publish_in_unixtime)
musicbox.create_table(True)

musicbox.create(publish_in=publish_in_unixtime,
                publish_data=str({"test": "1223"}))
