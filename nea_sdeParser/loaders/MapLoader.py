from tqdm.notebook import tqdm, trange
import yaml as ym

from .BaseLoader import Loader
from nea_schema.sde.map import Region, Constellation, System, Planet, Moon, Belt, Station, Stargate

class MapLoader(Loader):
    data_path = 'sde/fsd/universe'
    delete_sequence = [
        Stargate, Station, Belt, Moon,
        Planet, System, Constellation, Region
    ]
    
    def __init__(self, sde_path, sql_settings_path, verbose=False):
        super().__init__(sde_path, sql_settings_path, verbose=verbose)
        self.data = {
            'regions': [],
            'constellations': [],
            'systems': [],
            'planets': [],
            'moons': [],
            'belts': [],
            'stargates': [],
            'stations': [],
        }
    
    def parse_data(self):
        map_path = self.sde_path / self.data_path

        path_parse = [path for path in map_path.glob('**/*') if not path.is_dir()]
        t = tqdm(path_parse, leave=False) if self.verbose else path_parse
        for path in t:
            if path.name == 'region.staticdata':
                with open(path) as file:
                    region_data = ym.load(file, Loader=ym.SafeLoader)
                    self.data['regions'].append(Region.sde_parse(region_data))

            elif path.name == 'constellation.staticdata':
                with open(path) as file:
                    constellation_data = {
                        **ym.load(file, Loader=ym.SafeLoader),
                        'regionID': self.data['regions'][-1].region_id
                    }
                    self.data['constellations'].append(Constellation.sde_parse(constellation_data))

            elif path.name == 'solarsystem.staticdata':
                with open(path) as file:
                    system_data = {
                        **ym.load(file, Loader=ym.SafeLoader),
                        'constellationID': self.data['constellations'][-1].constellation_id,
                    }
                    self.data['systems'].append(System.sde_parse(system_data))
                    
                    for planet_id, planet_data in system_data.get('planets',{}).items():
                        planet_data = {
                            **planet_data,
                            'planetID': planet_id,
                            'solarSystemID': self.data['systems'][-1].system_id,
                        }
                        self.data['planets'].append(Planet.sde_parse(planet_data))
                        
                        for moon_id, moon_data in planet_data.get('moons', {}).items():
                            moon_data = {
                                **moon_data,
                                'moonID': moon_id,
                                'planetID': planet_id,
                            }
                            self.data['moons'].append(Moon.sde_parse(moon_data))
                            
                            for station_id, station_data in moon_data.get('npcStations', {}).items():
                                station_data = {
                                    **station_data,
                                    'npcStationID': station_id,
                                    'planetID': planet_id,
                                }
                                self.data['stations'].append(Station.sde_parse(station_data))
                                
                        for belt_id, belt_data in planet_data.get('asteroidBelts', {}).items():
                            belt_data = {
                                **belt_data,
                                'asteroidBeltID': belt_id,
                                'planetID': planet_id,
                            }
                            self.data['belts'].append(Belt.sde_parse(belt_data))
                            
                        for station_id, station_data in planet_data.get('npcStations', {}).items():
                            station_data = {
                                **station_data,
                                'npcStationID': station_id,
                                'planetID': planet_id,
                            }
                            self.data['stations'].append(Station.sde_parse(station_data))
                            
                    for stargate_id, stargate_data in system_data.get('stargates', {}).items():
                        stargate_data = {
                            **stargate_data,
                            'source': stargate_id,
                            'solarSystemID': self.data['systems'][-1].system_id,
                        }
                        self.data['stargates'].append(Stargate.sde_parse(stargate_data))
        
    def delete_old_data(self, conn):
        for schema in self.delete_sequence:
            conn.query(schema).delete()
        conn.commit()
        
    def load_new_data(self, conn):
        for data_list in self.data.values():
            conn.bulk_save_objects(data_list)
        conn.commit()
        