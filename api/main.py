
import asyncio
import os

from aiohttp import web

from config.setup_config import setup_config
from database.setup_database import setup_database
from routes import setup_routes

SOCKET_RIGHTS = 0o22


def setup_app(loop=None):
    app = web.Application(loop=loop)
    setup_config(app)
    setup_database(app)
    setup_routes(app)
    loop = asyncio.get_event_loop()
    return app

if __name__ == '__main__':
    OLD_UMASK = os.umask(SOCKET_RIGHTS)
    os.umask(0)
    try:
        web.run_app(app=setup_app())
    finally:
        os.umask(OLD_UMASK)
