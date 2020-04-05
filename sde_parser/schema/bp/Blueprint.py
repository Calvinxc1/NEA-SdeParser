from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER as Integer
from sqlalchemy.orm import relationship

from .. import _Base

class Blueprint(_Base):
    __tablename__ = 'bp_Blueprint'
    
    ## Columns
    blueprint_id = Column(Integer(unsigned=True), primary_key=True, autoincrement=False)
    type_id = Column(Integer(unsigned=True), ForeignKey('inv_Type.type_id', ondelete='CASCADE'))
    max_production_limit = Column(Integer(unsigned=True))
    
    ## Relationships
    type = relationship('Type')
    activity = relationship('Activity', back_populates='blueprint')
    
    @classmethod
    def sde_parse(cls, sde_record):
        sde_obj = cls(
            blueprint_id=sde_record.get('blueprintID'),
            type_id=sde_record.get('blueprintTypeID'),
            max_production_limit=sde_record.get('maxProductionLimit'),
        )
        return sde_obj