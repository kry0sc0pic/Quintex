from flask_restful import Resource
import json
from dti.dti import sendTokens
# import threading
from flask import request
class Tokens(Resource):

    def post(self):
        body = request.data.decode('utf-8')
        body = json.loads(body)
        tokens = body['tokens']
        print(tokens)
        sendTokens(tokens)
        return {},200
        
    