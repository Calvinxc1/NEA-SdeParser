import pandas as pd
from sqlalchemy.orm import sessionmaker
from tqdm.notebook import tqdm, trange
import yaml as ym

from .BaseLoader import Loader
from ..schema.inv import Category, Group, Type, MarketGroup, Reprocess

class InventoryLoader(Loader):
    data_paths = {
        'marketGroup': {
            'schema': MarketGroup,
            'path': 'sde/fsd/marketGroups.yaml',
        },
        'category': {
            'schema': Category,
            'path': 'sde/fsd/categoryIDs.yaml',
        },
        'group': {
            'schema': Group,
            'path': 'sde/fsd/groupIDs.yaml',
        },
        'type': {
            'schema': Type,
            'path': 'sde/fsd/typeIDs.yaml',
        },
        'reprocess': {
            'schema': Reprocess,
            'path': 'sde/fsd/typeMaterials.yaml'
        }
    }
    delete_sequence = [
        Type, Group, Category, MarketGroup
    ]
    reproc_skips = [
        53839, 53853, 53854, 53855, 53856, 53857, 53890, 53891, 53892,
        53893, 53894, 53895, 53896, 53897, 53898, 53899, 53900, 53901,
        53902, 53903, 53904, 53905, 53906, 53907
    ]
    
    def __init__(self, sde_path, sql_settings_path, verbose=False):
        super().__init__(sde_path, sql_settings_path, verbose=verbose)
        self.data = {
            'marketGroup': [],
            'category': [],
            'group': [],
            'type': [],
            'reprocess': [],
        }
    
    def parse_data(self):
        for key, val in self.data_paths.items():
            data_path = self.sde_path / val['path']
        
            with open(data_path) as file:
                data = ym.load(file, Loader=ym.SafeLoader)
                
            if key == 'reprocess':
                data = [
                    {'typeID':key, **subval}
                    for key, val in data.items()
                    for subval in val['materials']
                    if key not in self.reproc_skips
                ]
            elif key == 'marketGroup':
                data = self.process_market(pd.DataFrame([
                    {'marketGroupID': subkey, **subval}
                    for subkey, subval in data.items()
                ]))
            else:
                data = [
                    {'{}ID'.format(key): subkey, **subval}
                    for subkey, subval in data.items()
                ]
                
            if self.verbose: data = tqdm(data, leave=False)
            for data_file in data:
                self.data[key].append(val['schema'].sde_parse(data_file))
                
    @staticmethod
    def process_market(market_data):
        new_structure = []
        inactive_ids = []
        current_ids = market_data.loc[pd.isnull(market_data['parentGroupID'])]
        while len(inactive_ids) < len(market_data):
            new_structure.extend([row.to_dict() for _, row in current_ids.iterrows()])
            inactive_ids.extend(current_ids['marketGroupID'])
            current_ids = market_data.loc[market_data['parentGroupID'].isin(current_ids['marketGroupID'])]
        filtered_structure = []
        for row in new_structure:
            new_row = {}
            for key, val in row.items():
                if pd.isnull(val): continue
                new_row[key] = val
            filtered_structure.append(new_row)
        return filtered_structure
        
    def process_data(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        self.delete_old_data(session)
        self.load_new_data(session)
        session.close()
        
    def delete_old_data(self, session):
        for schema in self.delete_sequence:
            session.query(schema).delete()
        session.commit()
        
    def load_new_data(self, session):
        for key, data_list in self.data.items():
            session.bulk_save_objects(data_list)
        session.commit()
        