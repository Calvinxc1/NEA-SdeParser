from flask import Flask
from flask_restful import Api

from .resource import SDE
from .settings import SDE_SETTINGS

app = Flask(__name__)
api = Api(app)

api.add_resource(
    SDE, '/sde',
    resource_class_kwargs=SDE_SETTINGS,
)