from bottle import hook, route, response, request, post, run, debug
from playhouse.postgres_ext import *
import re
import json

user = 'postgres'
password = 'Pasd@1234'
db_name = 'musicbox'

db = PostgresqlDatabase(
    db_name, user=user,
    password=password,
    host='localhost'
)


class musicbox_publications(Model):
    channel_id = IntegerField()
    publish_in = IntegerField()
    published_in = IntegerField(default=0)
    publish_data = JSONField()

    class Meta:
        database = db  # This model uses the "people.db" database.

musicbox_publications.create_table(True)

#curl --header "Content-Type: application/json"  --request POST --data '{"publish_in":12321321,"channel_id":12,"channel_data":{"albom_cover":"File_path","track_file":"Track_file_pach","track_name":"Test track name","artist_name":"test artist name","publish_in":"123653543"}}'  http://127.0.0.1:8280/publication/add



def create_new_publication(channel_id, channel_data, publish_in):
    try:
        if channel_data['albom_cover'] is None:
            raise ValueError
        if channel_data['track_file'] is None:
            raise ValueError
        if channel_data['artist_name'] is None:
            raise ValueError
        if channel_data['track_name'] is None:
            raise ValueError
    except (TypeError, KeyError):
        raise ValueError
    publish_id = musicbox_publications.create(
        channel_id=channel_id,
        publish_in=publish_in,
        publish_data=channel_data
    )
    return {"publish_id":publish_id}

@route('/publication/add', method='POST')
def creation_handler():
    """Handles name creation"""

    try:
        try:
            data = request.json
        except:
            raise ValueError

        if data is None:
            raise ValueError

        try:
            if data['channel_id'] is None:
                raise ValueError
            channel_id = data['channel_id']
        except (TypeError, KeyError):
            raise ValueError

        try:
            if data['publish_in'] is None:
                raise ValueError
            publish_in = data['publish_in']
        except (TypeError, KeyError):
            raise ValueError


        try:
            if data['channel_data'] is None:
                raise ValueError
            channel_data = data['channel_data']
        except (TypeError, KeyError):
            raise ValueError



    except KeyError:
        # if name already exists, return 409 Conflict
        response.status = 409
        return

    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'response': 'OK'})

@route('/publication/update', method='POST')
def creation_handler():
    pass

@route('/publication/list', method='GET')
def creation_handler():
    pass

@route('/publication/get', method='GET')
def creation_handler():
    pass


@route('/channel/list', method='GET')
def creation_handler():
    pass

@route('/channel/create', method='POST')
def creation_handler():
    pass



debug(True)
run(host='127.0.0.1', port=8280, reload=True)
