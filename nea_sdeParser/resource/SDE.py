from flask import request
from flask_restful import Resource
from hashlib import sha256
from multiprocessing import Process
from shutil import rmtree

from .. import ETL
from .. import Unzipper

class SDE(Resource):
    def __init__(self, sde_path, sql_params, verbose=False):
        self.sde_path = sde_path
        self.sql_params = sql_params
        self.verbose = verbose
        
    def post(self):
        data = request.get_data()
        data_hash = sha256(data).hexdigest()
        
        p = Process(target=self._load_sde, args=(data,))
        p.start()        
        
        return {'hash': data_hash}, 202
    
    def _load_sde(self, data):
        Unzipper(self.sde_path, self.verbose).unzip_sde()
        ETL(self.sde_path, self.sql_params, self.verbose).run_etl()
        rmtree(self.sde_path)