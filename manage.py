from wsgi import Application
from urls import urls
from middlewares import middlewares
from migrations import make_migrations

make_migrations()
application = Application(urls, middlewares)
