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

def create_channel(name,chat_id,token):
    channel_id = Channels.create(
        channel_name=name,
        chat_id=chat_id,
        token=token
    ).id
    return channel_id

def delete_channel(channel_id):
    return Channels.delete().where(Channels.id == channel_id).execute()

def list_channels():
    query = Channels.select()
    channels_info = []
    for channel in query:
        channels_info.append(
            {
                'channel_id':channel.id,
                'channel_name': channel.channel_name,
                'chat_id': channel.chat_id,
                'token': channel.token
             }
        )
    print(channels_info)
    return channels_info


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
    return json.dumps(list_channels())


#curl --header "Content-Type: application/json"  --request POST --data '{"name":"test","chat_id":"-1001351914963","token":"735879873:AAFMHSGN9khiTjjf5G5L5mtHeygdI7hSwPc"}'  http://0.0.0.0:8888/channel/create

@route('/channel/create', method='POST')
def creation_handler():
    try:
        try:
            data = request.json
        except:
            raise ValueError

        if data is None:
            raise ValueError

        try:
            if data['name'] is None:
                raise ValueError
            name = data['name']
        except (TypeError, KeyError):
            raise ValueError

        try:
            if data['chat_id'] is None:
                raise ValueError
            chat_id = data['chat_id']
        except (TypeError, KeyError):
            raise ValueError

        try:
            if data['token'] is None:
                raise ValueError
            token = data['token']
        except (TypeError, KeyError):
            raise ValueError
        channel_id = create_channel(name,chat_id,token)


    except KeyError:
        # if name already exists, return 409 Conflict
        response.status = 409
        return

    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'response': 'OK',
                       'channel_id': channel_id})


@route('/channel/del/<channel_id>', method='GET')
def creation_handler(channel_id):
    return json.dumps(
        {
            'return': str(delete_channel(channel_id))

        }
        )

run(
    host='0.0.0.0',
    port=config.COMMON.api_port,
    debug=True,
    reloader=True
)
