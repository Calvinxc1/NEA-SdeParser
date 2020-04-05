import json as js
from pathlib import Path
from sqlalchemy import create_engine

class Loader:
    def __init__(self, sde_path, sql_settings_path, verbose=False):
        self.sde_path = Path(sde_path)
        self.engine = self.load_engine(sql_settings_path)
        self.verbose = verbose
        
    @staticmethod
    def load_engine(sql_settings_path):
        with open(Path(sql_settings_path)) as file:
            engine = create_engine('{engine}://{user}:{passwd}@{host}/{db}'.format(**js.load(file)))
        return engine
