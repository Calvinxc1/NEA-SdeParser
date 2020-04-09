from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER as Integer, DOUBLE as Double, BOOLEAN as Boolean, FLOAT as Float, VARCHAR as VarChar
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from .. import _Base

class Belt(_Base):
    __tablename__ = 'map_Belt'
    
    ## Columns
    belt_id = Column(Integer(unsigned=True), primary_key=True, autoincrement=False)
    type_id = Column(Integer(unsigned=True), ForeignKey('inv_Type.type_id'))
    name_id = Column(Integer(unsigned=True))
    planet_id = Column(Integer(unsigned=True), ForeignKey('map_Planet.planet_id'))
    density = Column(Double(unsigned=False))
    eccentricity = Column(Double(unsigned=False))
    escape_velocity = Column(Double(unsigned=False))
    fragmented = Column(Boolean)
    life = Column(Double(unsigned=False))
    locked = Column(Boolean)
    mass_dust = Column(Double(unsigned=False))
    mass_gas = Column(Double(unsigned=False))
    orbit_period = Column(Double(unsigned=False))
    orbit_radius = Column(Double(unsigned=False))
    pressure = Column(Double(unsigned=False))
    radius = Column(Double(unsigned=False))
    rotation_rate = Column(Double(unsigned=False))
    spectral_class = Column(VarChar(length=3))
    surface_gravity = Column(Double(unsigned=False))
    temperature = Column(Double(unsigned=False))
    pos_x = Column(Double(unsigned=False))
    pos_y = Column(Double(unsigned=False))
    pos_z = Column(Double(unsigned=False))
    
    ## Relationships
    name = relationship(
        'Name',
        primaryjoin='Belt.belt_id==Name.item_id',
        foreign_keys='Name.item_id',
        uselist=False,
    )
    planet = relationship('Planet', back_populates='belt')
    type = relationship('Type')
    
    ## Aliased Columns
    belt_name = association_proxy('item_name', 'item_name')
    
    @classmethod
    def sde_parse(cls, sde_record):
        sde_obj = cls(
            belt_id=sde_record.get('asteroidBeltID'),
            type_id=sde_record.get('typeID'),
            name_id=sde_record.get('asteroidBeltNameID'),
            planet_id=sde_record.get('planetID'),
            density=sde_record.get('statistics', {}).get('density'),
            eccentricity=sde_record.get('statistics', {}).get('eccentricity'),
            escape_velocity=sde_record.get('statistics', {}).get('escapeVelocity'),
            fragmented=sde_record.get('statistics', {}).get('fragmented'),
            life=sde_record.get('statistics', {}).get('life'),
            locked=sde_record.get('statistics', {}).get('locked'),
            mass_dust=sde_record.get('statistics', {}).get('massDust'),
            mass_gas=sde_record.get('statistics', {}).get('massGas'),
            orbit_period=sde_record.get('statistics', {}).get('orbitPeriod'),
            orbit_radius=sde_record.get('statistics', {}).get('orbitRadius'),
            pressure=sde_record.get('statistics', {}).get('pressure'),
            radius=sde_record.get('statistics', {}).get('radius'),
            rotation_rate=sde_record.get('statistics', {}).get('rotationRate'),
            spectral_class=sde_record.get('statistics', {}).get('spectralClass'),
            surface_gravity=sde_record.get('statistics', {}).get('surfaceGravity'),
            temperature=sde_record.get('statistics', {}).get('temperature'),
            pos_x=sde_record.get('position', [None, None, None])[0],
            pos_y=sde_record.get('position', [None, None, None])[1],
            pos_z=sde_record.get('position', [None, None, None])[2],
        )
        return sde_obj
