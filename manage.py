from wsgi import Application
from urls import urls
from middlewares import middlewares

application = Application(urls, middlewares)
