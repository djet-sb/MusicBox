import os

from collections import namedtuple

try:
    Common = namedtuple('Common', 'sentry_dsn, service_name')
    COMMON = Common(
        sentry_dsn=os.environ['SCHEDULE_SENTRY_DSN'],
        service_name='schedule',
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