
import time
import datetime
from flask import g, request, current_app

def start_timer():
    g.start = time.time()


def log_request(response):

    now = time.time()
    duration = round(now - g.start, 2)
    dt = datetime.datetime.fromtimestamp(now)
    timestamp = dt.isoformat()

    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    host = request.host.split(':', 1)[0]
    args = dict(request.args)

    log_params = [
            ('method', request.method),
            ('path', request.path),
            ('status', response.status_code),
            ('duration', duration),
            ('time', timestamp),
            ('ip', ip),
            ('host', host),
            ('params', args)
        ]

    request_id = request.headers.get('X-Request-ID')
    if request_id:
        log_params.append(('request_id', request_id, 'yellow'))

    parts = []
    for name, value in log_params:
        part = "{}={}".format(name, value)
        parts.append(part)
    line = " ".join(parts)

    current_app.logger.info(line)

    return response


def init_logging(app):
    app.logger.info(f"Adding request logging before/after handlers.")
    app.before_request(start_timer)
    app.after_request(log_request)
