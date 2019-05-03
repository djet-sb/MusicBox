from bottle import route, response, request, run
from playhouse.postgres_ext import *
import config

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


# curl --header "Content-Type: application/json"  --request POST --data '{"publish_in":12321321,"channel_id":12,"channel_data":{"album_cover":"File_path","track_file":"Track_file_pach","track_name":"Test track name","artist_name":"test artist name","publish_in":"123653543"}}'  http://127.0.0.1:8280/publication/add

@route('/', method='POST')
def creation_handler():
    pass


run(
    host='0.0.0.0',
    port=config.COMMON.api_port,
    debug=True,
    reloader=True
)
