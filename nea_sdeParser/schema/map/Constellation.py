from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER as Integer, DOUBLE as Double
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from .. import _Base

class Constellation(_Base):
    """ Schema for the map_Region table
    
    Columns
    -------
    constellation_id: Integer, Unsigned - Primary Key
        The unique identifier for the constellation
    constellation_name: Aliased from ItemName.item_name
        The name of the region
    region_id: Integer, Unsigned - Foreign Key (Region.region_id)
        The identifier for the region the constellation is in
    name_id: Integer, Unsigned
        Name ID number
    faction_id: Integer, Unsigned
        Faction ID number
    wormhole_class_id: Integer, Unsigned
        Wormhole Class ID
    radius: Double, Signed
        The spatial radius containing the constellation
    min_x/y/z: Double, Signed
        XYZ vector for the constellation's min coordinates in the universe frame
    center_x/y/z: Double, Signed
        XYZ vector for the constellation's origin coordinates in the universe frame
    max_x/y/z: Double, Signed
        XYZ vector for the constellation's max coordinates in the universe frame
        
    Relationships
    -------------
    item_name: Constellation.constellation_id <> ItemName.item_id
    region: Constellation.region_id <> Region.region_id
    """
    
    __tablename__ = 'map_Constellation'
    
    ## Columns
    constellation_id = Column(Integer(unsigned=True), primary_key=True, autoincrement=False)
    region_id = Column(Integer(unsigned=True), ForeignKey('map_Region.region_id'))
    name_id = Column(Integer(unsigned=True))
    faction_id = Column(Integer(unsigned=True))
    wormhole_class_id = Column(Integer(unsigned=True))
    radius = Column(Double(unsigned=False))
    min_x = Column(Double(unsigned=False))
    min_y = Column(Double(unsigned=False))
    min_z = Column(Double(unsigned=False))
    center_x = Column(Double(unsigned=False))
    center_y = Column(Double(unsigned=False))
    center_z = Column(Double(unsigned=False))
    max_x = Column(Double(unsigned=False))
    max_y = Column(Double(unsigned=False))
    max_z = Column(Double(unsigned=False))
    
    ## Relationships
    name = relationship(
        'Name',
        primaryjoin='Constellation.constellation_id==Name.item_id',
        foreign_keys='Name.item_id',
        uselist=False,
    )
    region = relationship('Region', back_populates='constellation')
    system = relationship('System', back_populates='constellation')
    
    ## Aliased Columns
    constellation_name = association_proxy('item_name', 'item_name')
    
    @classmethod
    def sde_parse(cls, sde_record):
        """ Auto-parser for EVE Static Data Export file(s)
        
        Parameters
        ----------
        sde_record: dict
            YAML-parsed dictionary of a specific constellation
            
        Returns
        -------
        Constellation:
            A fully-populated Constellation object
        """
        
        sde_obj = cls(
            constellation_id=sde_record.get('constellationID'),
            region_id=sde_record.get('regionID'),
            name_id=sde_record.get('nameID'),
            faction_id=sde_record.get('factionID'),
            wormhole_class_id=sde_record.get('wormholeClassID'),
            radius=sde_record.get('radius'),
            min_x=sde_record.get('min', [None, None, None])[0],
            min_y=sde_record.get('min', [None, None, None])[1],
            min_z=sde_record.get('min', [None, None, None])[2],
            center_x=sde_record.get('center', [None, None, None])[0],
            center_y=sde_record.get('center', [None, None, None])[1],
            center_z=sde_record.get('center', [None, None, None])[2],
            max_x=sde_record.get('max', [None, None, None])[0],
            max_y=sde_record.get('max', [None, None, None])[1],
            max_z=sde_record.get('max', [None, None, None])[2],
        )
        return sde_obj