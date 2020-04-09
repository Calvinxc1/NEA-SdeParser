from .loaders import ItemLoader, InventoryLoader, MapLoader, BlueprintLoader

class ETL:
    loaders = [ItemLoader, InventoryLoader, MapLoader, BlueprintLoader]
    
    def __init__(self, sde_path, sql_params, verbose=False):
        self.sde_path = sde_path
        self.sql_params = sql_params
        self.verbose = verbose
        
    def run_etl(self):
        for loader in self.loaders:
            self._run_loader(loader)
        
    def _run_loader(self, Loader):
        loader = Loader(self.sde_path, self.sql_params, verbose=self.verbose)
        loader.parse_data()
        loader.process_data()