from playhouse.postgres_ext import *
import config

user = config.DATABASE.user
password = config.DATABASE.password
db_name = config.DATABASE.db_name
db_host = config.DATABASE.host

db = PostgresqlDatabase(
    db_name, user=user,
    password=password,
    host=db_host
)


class musicbox(Model):
    publish_in = DateField()
    published_in = DateField()
    publish_data = JSONField()
    class Meta:
        database = db  # This model uses the "people.db" database.
try:
    musicbox.create_table(True)
except OperationalError as err:
    print(err)
    exit(1)

