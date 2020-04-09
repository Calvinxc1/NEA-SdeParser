import json as js
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Loader:
    def __init__(self, sde_path, sql_params, verbose=False):
        self.sde_path = Path(sde_path)
        self.engine = self.load_engine(sql_params)
        self.verbose = verbose
        
    @staticmethod
    def load_engine(sql_params):
        engine = create_engine('{engine}://{user}:{passwd}@{host}/{db}'.format(**sql_params))
        return engine
    
    def process_data(self):
        Session, conn = self.build_session(self.engine)
        self.delete_old_data(conn)
        self.load_new_data(conn)
        conn.close()
    
    @staticmethod
    def build_session(engine):
        Session = sessionmaker(bind=engine)
        conn = Session()
        conn.execute('SET SESSION foreign_key_checks=0;')
        return Session, conn