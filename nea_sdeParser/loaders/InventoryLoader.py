import pandas as pd
from tqdm.notebook import tqdm, trange
import yaml as ym

from .BaseLoader import Loader
from nea_schema.sde.inv import Name, Category, Group, Type, MarketGroup, Reprocess

class InventoryLoader(Loader):
    data_paths = {
        'name': {
            'schema': Name,
            'path': 'sde/bsd/invNames.yaml',
        },
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
        },
    }
    delete_sequence = [
        Type, Group, Category, MarketGroup, Reprocess, Name
    ]
    reproc_skips = [
        53839, 53853, 53854, 53855, 53856, 53857, 53890, 53891, 53892,
        53893, 53894, 53895, 53896, 53897, 53898, 53899, 53900, 53901,
        53902, 53903, 53904, 53905, 53906, 53907
    ]
    
    def __init__(self, sde_path, sql_settings_path, verbose=False):
        super().__init__(sde_path, sql_settings_path, verbose=verbose)
        self.data = {
            'name': [],
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
            
            if key == 'name':
                pass
            
            elif key == 'reprocess':
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
            
            self.data[key].extend([
                val['schema'].sde_parse(data_file)
                for data_file in data
            ])
                
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
        
    def delete_old_data(self, conn):
        for schema in self.delete_sequence:
            conn.query(schema).delete()
        conn.commit()
        
    def load_new_data(self, conn):
        for key, data_list in self.data.items():
            conn.bulk_save_objects(data_list)
        conn.commit()
        