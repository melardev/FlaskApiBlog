import sys
import time

from flask_jwt import _default_jwt_decode_handler, _default_request_handler
from flask import _request_ctx_stack
from blog_api.factory import app
from shared.security import identity_handler

start_time = 0


@app.before_request
def before_req():
    start_time = time.clock()
    jwt = _default_request_handler()
    if jwt is not None:
        try:
            decoded_jwt = _default_jwt_decode_handler(jwt)
            _request_ctx_stack.top.current_identity = identity_handler(decoded_jwt)
        except Exception, e:
            pass
    global start_time


@app.after_request
def after_req(response):
    end_time = time.clock()
    elapsed = (end_time - start_time) * 1000
    sys.stdout.write('Request took %d milliseconds\n' % elapsed)
    return response
