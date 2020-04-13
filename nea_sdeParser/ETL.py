from sqlalchemy import create_engine
from tqdm.notebook import tqdm

from .loaders import InventoryLoader, MapLoader, BlueprintLoader

class ETL:
    loaders = [InventoryLoader, MapLoader, BlueprintLoader]
    
    def __init__(self, sde_path, sql_params, verbose=False):
        self.sde_path = sde_path
        self.sql_params = sql_params
        self.verbose = verbose
        
    def run_etl(self):
        t = tqdm(self.loaders) if self.verbose else self.loaders
        for loader in t:
            self._run_loader(loader)
        
    def _run_loader(self, Loader):
        loader = Loader(self.sde_path, self.sql_params, verbose=self.verbose)
        loader.parse_data()
        loader.process_data()