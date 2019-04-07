from bottle import route, request, abort
import bottle
import tempfile
import telegram
from selectel.storage import Container
container = Container("82926_music_box", "IPr6ugmaF6", "MusicBOX")
from raven import Client
from raven.contrib.bottle import Sentry
app = bottle.app()
app.catchall = False
client = Client('https://8b241f6ae1794b8b897b1434dfb4b16e:9cb3ef16daa04889baf7d5348f7e12e8@sentry.io/1422595')
app = Sentry(app, client)

def download_cdn_file(path_file_cdn):
    file = container.get(path_file_cdn)
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    with open(temp_file.name, 'wb') as f:
        f.write(file)
    return temp_file.name

def make_telegram_music_post(albom_cover,track_performer, track_title,track_caption, track_file,chat_id,token):
    mp3_file = open(download_cdn_file(track_file), 'rb')
    img_file = download_cdn_file(albom_cover)
    bot = telegram.Bot(token=token)
   # bot.send_photo(
   #     chat_id=chat_id,
  #      photo=open(img_file, 'rb')
   # )
    bot.send_audio(timeout=60,
                   chat_id=chat_id,
                   title=track_title,
                   caption=track_caption,
                   parse_mode='Markdown',
                   performer="TransConveer % " + track_performer,
                   audio=mp3_file
         )

# make_telegram_music_post(albom_cover="/rap_channel/Utilities-X11-icon.png",
#                         track_performer="Dan Farber",
#                         track_title="Don't Touch                                             ",
#                         track_caption="`Artist:  Dan Farber\nName: Don't Touch\nLabel:  Deep Palma\nDate:   15.05.2017`\n#electronic",
#                         track_file="/rap_channel/ЕА7 - Magic Phase - Impossible Love.mp3",
#                         chat_id="-1001351914963",
#                         token="735879873:AAFMHSGN9khiTjjf5G5L5mtHeygdI7hSwPc"
#                         )

#curl --header "Content-Type: application/json"  --request POST --data '{"albom_cover":"/rap_channel/Utilities-X11-icon.png","track_performer":"Dan Farber","track_title":"Dont Touch","track_caption":"test","track_file":"/rap_channel/ЕА7 - Magic Phase - Impossible Love.mp3","chat_id":"-1001351914963","token":"735879873:AAFMHSGN9khiTjjf5G5L5mtHeygdI7hSwPc"}'  http://0.0.0.0:8280/publish


@route('/publish', method='POST')
def do_publish():
    try:
        albom_cover = request.json['albom_cover']
        track_performer = request.json['track_performer']
        track_title = request.json['track_title']
        track_caption = request.json['track_caption']
        track_file = request.json['track_file']
        chat_id = request.json['chat_id']
        token = request.json['token']

        make_telegram_music_post(albom_cover,
                                 track_performer,
                                 track_title,
                                 track_caption,
                                 track_file,
                                 chat_id,
                                 token
                                 )
    except KeyError as  err:
        abort(404, f"KeyError: {err}")


bottle.debug(True)
bottle.run(app=app,host='127.0.0.1', port=8280, reload=True)

