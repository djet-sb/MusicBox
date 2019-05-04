
import os

from collections import namedtuple

try:
    Common = namedtuple('Common', 'sentry_dsn, service_name http_port')
    COMMON = Common(
        sentry_dsn=os.environ['UI_SENTRY_DSN'],
        service_name='ui',
        http_port=int(os.environ['UI_PORT']),
    )

    Database = namedtuple('Database',
                          'host,'
                          'db_name,'
                          'password,'
                          'user'
                          )
    DATABASE = Database(
        host=os.environ['DATABASE_HOST'],
        db_name=str(os.environ['DATABASE_NAME']),
        password=str(os.environ['DATABASE_PASSWORD']),
        user=str(os.environ['DATABASE_USER'])
    )
    Api = namedtuple('Api',
                          'host,'
                          'port'
                     )
    API = Api(
        host=os.environ['API_HOST'],
        port=os.environ['API_PORT']
    )
except Exception as ex:
    if isinstance(ex, KeyError):
        print(f'CRITICAL ERROR: Env variable {ex} not set')
    else:
        print(f'CRITICAL ERROR: {ex!r}')

    exit(1)
