
import os

from collections import namedtuple

try:
    Common = namedtuple('Common', 'sentry_dsn, service_name api_port')
    COMMON = Common(
        sentry_dsn=os.environ['API_SENTRY_DSN'],
        service_name='api',
        api_port=int(os.environ['API_PORT']),
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
except Exception as ex:
    if isinstance(ex, KeyError):
        print(f'CRITICAL ERROR: Env variable {ex} not set')
    else:
        print(f'CRITICAL ERROR: {ex!r}')

    exit(1)