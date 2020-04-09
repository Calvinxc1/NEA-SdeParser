from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER as Integer, DOUBLE as Double, BOOLEAN as Boolean, FLOAT as Float, VARCHAR as VarChar
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from .. import _Base

class System(_Base):
    __tablename__ = 'map_System'
    
    ## Columns
    system_id = Column(Integer(unsigned=True), primary_key=True, autoincrement=False)
    name_id = Column(Integer(unsigned=True))
    constellation_id = Column(Integer(unsigned=True), ForeignKey('map_Constellation.constellation_id'))
    desc_id = Column(Integer(unsigned=True))
    faction_id = Column(Integer(unsigned=True))
    wormhole_class_id = Column(Integer(unsigned=True))
    luminosity = Column(Float(unsigned=True))
    radius = Column(Double(unsigned=False))
    security = Column(Float(unsigned=False))
    security_class = Column(VarChar(length=2))
    visual_effect = Column(VarChar(length=25))
    border = Column(Boolean)
    corridor = Column(Boolean)
    fringe = Column(Boolean)
    hub = Column(Boolean)
    international = Column(Boolean)
    regional = Column(Boolean)
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
        primaryjoin='System.system_id==Name.item_id',
        foreign_keys='Name.item_id',
        uselist=False,
    )
    constellation = relationship('Constellation', back_populates='system')
    planet = relationship('Planet', back_populates='system')
    stargate = relationship('Stargate', back_populates='system')
    
    ## Aliased Columns
    system_name = association_proxy('item_name', 'item_name')
    
    @classmethod
    def sde_parse(cls, sde_record):
        sde_obj = cls(
            system_id=sde_record.get('solarSystemID'),
            name_id=sde_record.get('solarSystemNameID'),
            constellation_id=sde_record.get('constellationID'),
            wormhole_class_id=sde_record.get('wormholeClassID'),
            desc_id=sde_record.get('descriptionID'),
            faction_id=sde_record.get('factionID'),
            luminosity=sde_record.get('luminosity'),
            radius=sde_record.get('radius'),
            security=sde_record.get('security'),
            security_class=sde_record.get('securityClass'),
            visual_effect=sde_record.get('visualEffect'),
            border=sde_record.get('border'),
            corridor=sde_record.get('corridor'),
            fringe=sde_record.get('fringe'),
            hub=sde_record.get('hub'),
            international=sde_record.get('international'),
            regional=sde_record.get('regional'),
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
