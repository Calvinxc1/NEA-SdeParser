from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER as Integer, DOUBLE as Double, BOOLEAN as Boolean, FLOAT as Float, VARCHAR as VarChar
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from .. import _Base

class Moon(_Base):
    __tablename__ = 'map_Moon'
    
    ## Columns
    moon_id = Column(Integer(unsigned=True), primary_key=True, autoincrement=False)
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
    population = Column(Boolean)
    pressure = Column(Double(unsigned=False))
    radius = Column(Double(unsigned=False))
    rotation_rate = Column(Double(unsigned=False))
    spectral_class = Column(VarChar(length=3))
    surface_gravity = Column(Double(unsigned=False))
    temperature = Column(Double(unsigned=False))
    height_map_1 = Column(Integer(unsigned=True))
    height_map_2 = Column(Integer(unsigned=True))
    shader_preset = Column(Integer(unsigned=True))
    pos_x = Column(Double(unsigned=False))
    pos_y = Column(Double(unsigned=False))
    pos_z = Column(Double(unsigned=False))
    
    ## Relationships
    name = relationship(
        'Name',
        primaryjoin='Moon.moon_id==Name.item_id',
        foreign_keys='Name.item_id',
        uselist=False,
    )
    planet = relationship('Planet', back_populates='moon')
    type = relationship('Type')
    
    ## Aliased Columns
    moon_name = association_proxy('item_name', 'item_name')
    
    @classmethod
    def sde_parse(cls, sde_record):
        sde_obj = cls(
            moon_id=sde_record.get('moonID'),
            type_id=sde_record.get('typeID'),
            name_id=sde_record.get('moonNameID'),
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
            population=sde_record.get('planetAttributes', {}).get('population'),
            pressure=sde_record.get('statistics', {}).get('pressure'),
            radius=sde_record.get('statistics', {}).get('radius'),
            rotation_rate=sde_record.get('statistics', {}).get('rotationRate'),
            spectral_class=sde_record.get('statistics', {}).get('spectralClass'),
            surface_gravity=sde_record.get('statistics', {}).get('surfaceGravity'),
            temperature=sde_record.get('statistics', {}).get('temperature'),
            height_map_1=sde_record.get('planetAttributes', {}).get('heightMap1'),
            height_map_2=sde_record.get('planetAttributes', {}).get('heightMap2'),
            shader_preset=sde_record.get('planetAttributes', {}).get('shaderPreset'),
            pos_x=sde_record.get('position', [None, None, None])[0],
            pos_y=sde_record.get('position', [None, None, None])[1],
            pos_z=sde_record.get('position', [None, None, None])[2],
        )
        return sde_obj
