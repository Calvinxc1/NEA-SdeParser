from sqlalchemy import Column, ForeignKey, ForeignKeyConstraint
from sqlalchemy.dialects.mysql import INTEGER as Integer, VARCHAR as VarChar, FLOAT as Float
from sqlalchemy.orm import relationship

from .. import _Base
from . import Activity

class Product(_Base):
    __tablename__ = 'bp_Product'
    
    ## Columns
    blueprint_id = Column(Integer(unsigned=True), primary_key=True, autoincrement=False)
    activity_type = Column(VarChar(length=17), primary_key=True, autoincrement=False)
    type_id = Column(Integer(unsigned=True), ForeignKey('inv_Type.type_id', ondelete='CASCADE'), primary_key=True, autoincrement=False)
    quantity = Column(Integer(unsigned=True))
    probability = Column(Float(unsigned=True), default=1)
    
    ## Foreign Key Constraint
    __table_args__ = (
        ForeignKeyConstraint(
            [blueprint_id, activity_type],
            [Activity.blueprint_id, Activity.activity_type],
            ondelete='CASCADE',
        ),
        {},
    )
    
    ## Relationships
    activity = relationship('Activity', back_populates='product')
    type = relationship('Type')
    
    @classmethod
    def sde_parse(cls, sde_record):
        sde_obj = cls(
            blueprint_id=sde_record.get('blueprintID'),
            activity_type=sde_record.get('activity_type'),
            type_id=sde_record.get('typeID'),
            quantity=sde_record.get('quantity'),
            probability=sde_record.get('probability'),
        )
        return sde_obj