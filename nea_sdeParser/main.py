from flask import Flask
from flask_restful import Api

from .resource import SDE
from config.config import sde_path, sql_params, verbose

app = Flask(__name__)
api = Api(app)

api.add_resource(
    SDE, '/',
    resource_class_args=[sde_path, sql_params, verbose],
)