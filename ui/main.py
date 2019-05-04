from bottle import route, run, TEMPLATE_PATH, request, jinja2_template as template, view, redirect
from Helpers.api import ChannelsHelper, PublicationHelper
import config
TEMPLATE_PATH.append('./templates')
channels = ChannelsHelper()
channels.set_channels()
publications = PublicationHelper()


@route('/', method='GET')
def creation_handler():
    return template('index.html', channels_list=channels.list())

@route('/channel/new', method='GET')
@view('index.html')
def creation_handler():
    return template('index.html', channels_list=channels.list(), type="channel_settings", channel_info={})

@route('/channel/create', method='POST')
@view('index.html')
def creation_handler():
    chat_id = request.forms.get('chat_id')
    channel_name = request.forms.get('channel_name')
    token = request.forms.get('token')
    id = channels.create(channel_name,chat_id,token)['channel_id']
    channels.set_channels()
    redirect(f"/channel/{id}", 302)


@route('/channel/delete/<id>', method='GET')
@view('index.html')
def creation_handler(id):
    channels.delete(id)
    channels.set_channels()
    return f"Channel {id} has by deleted"

@route('/channel/<id>', method='GET')
@view('index.html')
def creation_handler(id):
    channel_info = channels.get(id)
    publications.set_publication(id)
    print(f"asdasdsdas {publications.get()}")
    return template('index.html', channels_list=channels.list(), type="publication_list", channel_info=channel_info,
                    publications_info=publications.get()['publication_data'])

@route('/channel/settings/<id>', method='GET')
@view('index.html')
def creation_handler(id):
    channel_info = channels.get(id)
    return template('index.html', channels_list=channels.list(), type="channel_settings", channel_info=channel_info)

@route('/enter', method='GET')
def creation_handler():
    return template('enter.html')


run(
    host='0.0.0.0',
    port=config.COMMON.http_port,
    debug=True,
    reloader=True
)
