from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER as Integer
from sqlalchemy.orm import relationship

from .. import _Base

class Reprocess(_Base):
    __tablename__ = 'inv_Reprocess'
    
    ## Columns
    type_id = Column(Integer(unsigned=True), ForeignKey('inv_Type.type_id', ondelete='CASCADE'), primary_key=True, autoincrement=False)
    material_type_id = Column(Integer(unsigned=True), ForeignKey('inv_Type.type_id', ondelete='CASCADE'), primary_key=True, autoincrement=False)
    quantity = Column(Integer(unsigned=True))
    
    ## Relationships
    type = relationship('Type', foreign_keys='Reprocess.type_id')
    material_type = relationship('Type', foreign_keys='Reprocess.material_type_id')

    @classmethod
    def sde_parse(cls, sde_record):
        sde_obj = cls(
            type_id=sde_record.get('typeID'),
            material_type_id=sde_record.get('materialTypeID'),
            quantity=sde_record.get('quantity'),
        )
        return sde_obj