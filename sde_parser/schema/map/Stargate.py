from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER as Integer, DOUBLE as Double, BOOLEAN as Boolean, FLOAT as Float, VARCHAR as VarChar
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from .. import _Base

class Stargate(_Base):
    __tablename__ = 'map_Stargate'
    
    ## Columns
    stargate_id = Column(Integer(unsigned=True), primary_key=True, autoincrement=False)
    type_id = Column(Integer(unsigned=True), ForeignKey('inv_Type.type_id'))
    system_id = Column(Integer(unsigned=True), ForeignKey('map_System.system_id'))
    dest_stargate_id = Column(Integer(unsigned=True))
    pos_x = Column(Double(unsigned=False))
    pos_y = Column(Double(unsigned=False))
    pos_z = Column(Double(unsigned=False))
    
    ## Relationships
    name = relationship(
        'Name', uselist=False,
        primaryjoin='Stargate.stargate_id==Name.item_id',
        foreign_keys='Name.item_id',
    )
    system = relationship('System', back_populates='stargate')
    dest_stargate = relationship(
        'Stargate', uselist=False,
        primaryjoin='Stargate.dest_stargate_id==Stargate.stargate_id',
        foreign_keys='Stargate.stargate_id',
    )
    type = relationship('Type')
    
    ## Aliased Columns
    stargate_name = association_proxy('item_name', 'item_name')
    
    @classmethod
    def sde_parse(cls, sde_record):
        sde_obj = cls(
            stargate_id=sde_record.get('source'),
            type_id=sde_record.get('typeID'),
            system_id=sde_record.get('solarSystemID'),
            dest_stargate_id=sde_record.get('destination'),
            pos_x=sde_record.get('position', [None, None, None])[0],
            pos_y=sde_record.get('position', [None, None, None])[1],
            pos_z=sde_record.get('position', [None, None, None])[2],
        )
        return sde_obj
