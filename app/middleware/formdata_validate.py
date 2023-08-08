from werkzeug.wrappers import Request
from flask import request, jsonify
from validation import validate_structure, validate_int
import json
from flask_http_middleware import MiddlewareManager, BaseHTTPMiddleware


###    НЕ ИСПОЛЬЗУЕТСЯ    ###
class ValidateMiddleware(BaseHTTPMiddleware):
    def __init__(self):
        super().__init__()

    def dispatch(self, request, call_next):
        if 'file' in request.files:
            try:
                validate_structure(json.loads(request.form.get('data')), schema={
                            'chat_id': validate_int(min_value=0),
                            'user_id': validate_int(min_value=0)
                        })
                
                response = call_next(request)
                return response
            except:
                return jsonify({
                    'message': 'validation error'
                })
        else:
            response = call_next(request)
            return response
