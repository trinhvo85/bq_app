import os

APP_PORT = os.getenv("APP_PORT", "5050")

reload = True
bind = f"127.0.0.1:{APP_PORT}"
workers = 4
worker_class = 'gevent'
timeout = 3600