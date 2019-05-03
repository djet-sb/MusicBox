from bottle import route, response, request, run
from playhouse.postgres_ext import *
import json
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
    chat_id = IntegerField()
    token = TextField()

    class Meta:
        database = db  # This model uses the "people.db" database.


Channels.create_table(True)
Publications.create_table(True)


# curl --header "Content-Type: application/json"  --request POST --data '{"publish_in":12321321,"channel_id":12,"channel_data":{"album_cover":"File_path","track_file":"Track_file_pach","track_name":"Test track name","artist_name":"test artist name","publish_in":"123653543"}}'  http://127.0.0.1:8280/publication/add

def publication_data(publication_ids):
    query = Publications.select().where(Publications.id << publication_ids)
    publications = []
    for pub in query:
        publications.append(
            {
                'publish_id': pub.id,
                'channel_id': pub.channel_id,
                'publish_in': pub.publish_in,
                'published_in': pub.published_in,
                'publish_data': pub.publish_data
             }
        )
    return publications

def create_new_publication(channel_id, channel_data, publish_in):
    try:
        if channel_data['album_cover'] is None:
            raise ValueError
        if channel_data['track_file'] is None:
            raise ValueError
        if channel_data['artist_name'] is None:
            raise ValueError
        if channel_data['track_name'] is None:
            raise ValueError
    except (TypeError, KeyError):
        raise ValueError
    publish_id = Publications.create(
        channel_id=channel_id,
        publish_in=publish_in,
        publish_data=channel_data
    )
    return {"publish_id": publish_id}


def list_publication(channel_id):
    query = Publications.select().where(Publications.channel_id == channel_id)
    return [pub.id for pub in query]


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
        publish_id = create_new_publication(channel_id, channel_data, publish_in)


    except KeyError:
        # if name already exists, return 409 Conflict
        response.status = 409
        return

    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'response': 'OK',
                       'publish_id': str(publish_id)})


@route('/publication/update', method='POST')
def creation_handler():
    pass


@route('/publication/list/<channel_id>', method='GET')
def publication_handler(channel_id):
    #[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    return json.dumps(list_publication(channel_id))


@route('/publication/get', method='POST')
def publication_handler():
    try:
        try:
            data = request.json
        except:
            raise ValueError

        if data is None:
            raise ValueError

        try:
            if data['publication_ids'] is None:
                raise ValueError
            publication_ids = json.loads(data['publication_ids'])
        except (TypeError, KeyError):
            raise ValueError
        get_publication_data = publication_data(publication_ids)
    except KeyError:
        # if name already exists, return 409 Conflict
        response.status = 409
        return

    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'response': 'OK',
                       'publication_data': get_publication_data})


@route('/channel/list', method='GET')
def creation_handler():
    pass


@route('/channel/create', method='POST')
def creation_handler():
    pass


run(
    host='0.0.0.0',
    port=config.COMMON.api_port,
    debug=True,
    reloader=True
)
