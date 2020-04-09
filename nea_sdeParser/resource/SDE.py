from flask import request
from flask_restful import Resource
from hashlib import sha256
import io
from multiprocessing import Process
from pathlib import Path
from shutil import rmtree
import zipfile as zf

from ..ETL import ETL

class SDE(Resource):
    def __init__(self, config):
        self.sde_path = Path(config.sde_path)
        self.sql_params = config.sql_params
        self.verbose = config.verbose
        
    def post(self):
        data = request.get_data()
        data_hash = sha256(data).hexdigest()
        
        p = Process(target=self._load_sde, args=(data,))
        p.start()        
        
        return {'hash': data_hash}, 202
    
    def _load_sde(self, data):
        self._unzip_data(data)
        self._etl_data()
    
    def _unzip_data(self, data):
        zip_data = zf.ZipFile(io.BytesIO(data))
        
        if self.sde_path.exists():
            rmtree(self.sde_path)
            
        zip_data.extractall(self.sde_path)
        
    def _etl_data(self):
        etl = ETL(self.sde_path, self.sql_params, self.verbose)
        etl.run_etl()