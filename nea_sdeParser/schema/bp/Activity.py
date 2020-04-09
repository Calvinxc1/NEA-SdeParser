from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER as Integer, VARCHAR as VarChar
from sqlalchemy.orm import relationship

from .. import _Base

class Activity(_Base):
    __tablename__ = 'bp_Activity'
    
    ## Columns
    blueprint_id = Column(Integer(unsigned=True), ForeignKey('bp_Blueprint.blueprint_id', ondelete='CASCADE'), primary_key=True, autoincrement=False)
    activity_type = Column(VarChar(length=17), primary_key=True, autoincrement=False)
    time = Column(Integer(unsigned=True))
    
    ## Relationships
    blueprint = relationship('Blueprint', back_populates='activity')
    material = relationship('Material', back_populates='activity')
    product = relationship('Product', back_populates='activity')
    skill = relationship('Skill', back_populates='activity')
    
    @classmethod
    def sde_parse(cls, sde_record):
        sde_obj = cls(
            blueprint_id=sde_record.get('blueprintID'),
            activity_type=sde_record.get('activity_type'),
            time=sde_record.get('time'),
        )
        return sde_obj