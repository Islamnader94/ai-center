from flask import request, render_template, make_response
from flask_restful import Resource

class IndexResource(Resource):
    @staticmethod
    def get():
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'), 200, headers)