from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER as Integer, DOUBLE as Double, BOOLEAN as Boolean, FLOAT as Float, VARCHAR as VarChar
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from .. import _Base

class Station(_Base):
    __tablename__ = 'map_NpcStation'
    
    ## Columns
    station_id = Column(Integer(unsigned=True), primary_key=True, autoincrement=False)
    type_id = Column(Integer(unsigned=True), ForeignKey('inv_Type.type_id'))
    planet_id = Column(Integer(unsigned=True), ForeignKey('map_Planet.planet_id'))
    graphic_id = Column(Integer(unsigned=True))
    operation_id = Column(Integer(unsigned=True))
    owner_id = Column(Integer(unsigned=True))
    is_conquerable = Column(Boolean)
    use_operation_name = Column(Boolean)
    reprocessing_efficiency = Column(Float(unsigned=False))
    reprocessing_hangar_flag = Column(Integer(unsigned=False))
    reprocessing_stations_take = Column(Float(unsigned=False))
    pos_x = Column(Double(unsigned=False))
    pos_y = Column(Double(unsigned=False))
    pos_z = Column(Double(unsigned=False))
    
    ## Relationships
    name = relationship(
        'Name',
        primaryjoin='Station.station_id==Name.item_id',
        foreign_keys='Name.item_id',
        uselist=False,
    )
    planet = relationship('Planet', back_populates='station')
    type = relationship('Type')
    
    ## Aliased Columns
    station_name = association_proxy('item_name', 'item_name')
    
    @classmethod
    def sde_parse(cls, sde_record):
        sde_obj = cls(
            station_id=sde_record.get('npcStationID'),
            type_id=sde_record.get('typeID'),
            planet_id=sde_record.get('planetID'),
            graphic_id=sde_record.get('graphicID'),
            operation_id=sde_record.get('operationID'),
            owner_id=sde_record.get('ownerID'),
            is_conquerable=sde_record.get('isConquerable'),
            use_operation_name=sde_record.get('useOperationName'),
            reprocessing_efficiency=sde_record.get('reprocessingEfficiency'),
            reprocessing_hangar_flag=sde_record.get('reprocessingHangarFlag'),
            reprocessing_stations_take=sde_record.get('reprocessingStationsTake'),
            pos_x=sde_record.get('position', [None, None, None])[0],
            pos_y=sde_record.get('position', [None, None, None])[1],
            pos_z=sde_record.get('position', [None, None, None])[2],
        )
        return sde_obj
