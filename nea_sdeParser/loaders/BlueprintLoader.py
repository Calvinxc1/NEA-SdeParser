import pandas as pd
from tqdm.notebook import tqdm, trange
import yaml as ym

from .BaseLoader import Loader
from ..schema.bp import Blueprint, Activity, Material, Product, Skill

class BlueprintLoader(Loader):
    data_path = 'sde/fsd/blueprints.yaml'
    delete_sequence = [
        Skill, Product, Material, Activity, Blueprint
    ]
    drop_bp_ids = [
        3927, 37398, 37399, 37400, 37401, 37402, 37403, 37404,
        37405, 37406, 37407, 37408, 37409, 37425, 37426, 37427,
        37428, 37429, 37430, 37441, 37442
    ]
    
    def __init__(self, sde_path, sql_settings_path, verbose=False):
        super().__init__(sde_path, sql_settings_path, verbose=verbose)
        self.data = {
            'blueprint': [],
            'activity': [],
            'material': [],
            'product': [],
            'skill': [],
        }
    
    def parse_data(self):
        path = self.sde_path / self.data_path
        with open(path) as file:
            data = ym.load(file, Loader=ym.SafeLoader)
        
        t = data.items()
        if self.verbose: t = tqdm(t)
        for blueprint_id, blueprint_data in t:
            #if blueprint_id in self.drop_bp_ids: continue
            
            blueprint_data = {
                **blueprint_data,
                'blueprintID': blueprint_id,
            }
            self.data['blueprint'].append(Blueprint.sde_parse(blueprint_data))
            
            for activity_type, activity_data in blueprint_data.get('activities', {}).items():
                activity_data = {
                    **activity_data,
                    'blueprintID': blueprint_id,
                    'activity_type': activity_type,
                }
                self.data['activity'].append(Activity.sde_parse(activity_data))
                
                for material_data in activity_data.get('materials', []):
                    material_data = {
                        **material_data,
                        'blueprintID': blueprint_id,
                        'activity_type': activity_type,
                    }
                    self.data['material'].append(Material.sde_parse(material_data))
                
                for product_data in activity_data.get('products', []):
                    product_data = {
                        **product_data,
                        'blueprintID': blueprint_id,
                        'activity_type': activity_type,
                    }
                    self.data['product'].append(Product.sde_parse(product_data))
                    
                for skill_data in activity_data.get('skills', []):
                    skill_data = {
                        **skill_data,
                        'blueprintID': blueprint_id,
                        'activity_type': activity_type,
                    }
                    self.data['skill'].append(skill_data)
        
    def delete_old_data(self, conn):
        for schema in self.delete_sequence:
            conn.query(schema).delete()
        conn.commit()
        
    def load_new_data(self, conn):
        for key, data_list in self.data.items():
            if key == 'skill':
                data_list = [Skill.sde_parse(row.to_dict()) for _, row in pd.DataFrame(data_list).drop_duplicates().iterrows()]
            conn.bulk_save_objects(data_list)
        conn.commit()