from sqlalchemy.orm import sessionmaker
from tqdm.notebook import tqdm, trange
import yaml as ym

from .BaseLoader import Loader
from ..schema.itm import Name

class ItemLoader(Loader):
    data_path = 'sde/bsd/invNames.yaml'
    
    def __init__(self, sde_path, sql_settings_path, verbose=False):
        super().__init__(sde_path, sql_settings_path, verbose=verbose)
        self.data = []
    
    def parse_data(self):
        data_path = self.sde_path / self.data_path
        
        with open(data_path) as file:
            data = ym.load(file, Loader=ym.SafeLoader)
            if self.verbose: tqdm(data, leave=False)
            for data_file in data:
                self.data.append(Name.sde_parse(data_file))
        
    def process_data(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        self.delete_old_data(session)
        self.load_new_data(session)
        session.close()
        
    def delete_old_data(self, session):
        session.query(Name).delete()
        session.commit()
        
    def load_new_data(self, session):
        session.bulk_save_objects(self.data)
        session.commit()
        