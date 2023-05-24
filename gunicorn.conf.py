import os

def is_reload():
    r = bool(os.environ.get('RELOAD', False))
    print("is reload {}".format(r))
    return r

APP_PORT = os.getenv("APP_PORT", "5050")

reload = is_reload()
bind = f"127.0.0.1:{APP_PORT}"
workers = 13
worker_class = 'gevent'
timeout = 3600