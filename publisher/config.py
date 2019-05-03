
import os

from collections import namedtuple

try:
    Common = namedtuple('Common', 'sentry_dsn, service_name, publisher_port')
    COMMON = Common(
        sentry_dsn=os.environ['PUBLISHER_SENTRY_DSN'],
        publisher_port=os.environ['PUBLISHER_PORT'],
        service_name='publisher',

    )

    Cdn = namedtuple('Cdn',
                     'name,'
                     'password,'
                     'user'
                     )
    CDN = Cdn(
        name=os.environ['CDN_NAME'],
        password=str(os.environ['CDN_PASSWORD']),
        user=str(os.environ['CDN_USER']),
    )
except Exception as ex:
    if isinstance(ex, KeyError):
        print(f'CRITICAL ERROR: Env variable {ex} not set')
    else:
        print(f'CRITICAL ERROR: {ex!r}')

    exit(1)