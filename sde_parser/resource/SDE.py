from flask import request
from flask_restful import Resource
from hashlib import sha256
import io
from multiprocessing import Process
from pathlib import Path
from shutil import rmtree
import zipfile as zf

class SDE(Resource):
    def __init__(self, unzip_dir):
        self.unzip_path = self._build_unzip_path(unzip_dir)
        
    def _build_unzip_path(self, unzip_dir):
        unzip_path = Path(unzip_dir)
        return unzip_path
        
    def post(self):
        data = request.get_data()
        data_hash = sha256(data).hexdigest()
        
        p = Process(target=self._load_sde, args=(data,))
        p.start()        
        
        return {'hash': data_hash}, 202
    
    def _load_sde(self, data):
        self._unzip_data(data)
        
    
    def _unzip_data(self, data):
        zip_data = zf.ZipFile(io.BytesIO(data))
        
        if self.unzip_path.exists():
            rmtree(self.unzip_path)
            
        zip_data.extractall(self.unzip_path)
        
    def _etl_data(self):
        