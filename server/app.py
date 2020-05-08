from flask import Blueprint
from flask_restful import Api

from resources.ScannedData import ScannedDataResource
from resources.TemplateRender import IndexResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

template_bp = Blueprint('template', __name__)
template = Api(template_bp)

# Route
template.add_resource(IndexResource, '/')
api.add_resource(ScannedDataResource, '/List')
