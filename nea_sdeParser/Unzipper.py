import io
from pathlib import Path
from shutil import rmtree
import zipfile as zf

class Unzipper:
    def __init__(self, sde_path, verbose=False):
        self.sde_path = Path(sde_path)
        self.verbose = verbose
        
    def unzip_sde(self, bytes_file):
        self.purge_data()
        zip_data = zf.ZipFile(io.BytesIO(bytes_file))
        zip_data.extractall(self.sde_path)
        
    def purge_data(self):
        if self.sde_path.exists(): rmtree(self.sde_path)