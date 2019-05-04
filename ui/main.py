from bottle import route, run, TEMPLATE_PATH, request, jinja2_template as template, view
from Helpers.api import ChannelsHelper
import config
TEMPLATE_PATH.append('./templates')
channels = ChannelsHelper()
channels.set_channels()



@route('/', method='GET')
def creation_handler():
    return template('index.html', channels_list=channels.list())

@route('/channel/new', method='GET')
@view('index.html')
def creation_handler():

    return template('index.html', channels_list=channels.list(), type="channel_settings", channel_info={})


@route('/channel/<id>', method='GET')
@view('index.html')
def creation_handler(id):
    channel_info = channels.get(id)
    print(channel_info)
    return template('index.html', channels_list=channels.list(), type="publication_list", channel_info=channel_info)

@route('/channel/settings/<id>', method='GET')
@view('index.html')
def creation_handler(id):
    channel_info = channels.get(id)
    print(channel_info)
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
