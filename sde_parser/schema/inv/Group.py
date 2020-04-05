from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER as Integer, TINYTEXT as TinyText, BOOLEAN as Boolean
from sqlalchemy.orm import relationship

from .. import _Base

class Group(_Base):
    __tablename__ = 'inv_Group'
    
    ## Columns
    group_id = Column(Integer(unsigned=True), primary_key=True, autoincrement=False)
    group_name = Column(TinyText)
    category_id = Column(Integer(unsigned=True), ForeignKey('inv_Category.category_id'))
    icon_id = Column(Integer(unsigned=True))
    anchorable = Column(Boolean)
    anchored = Column(Boolean)
    fittable_non_singleton = Column(Boolean)
    published = Column(Boolean)
    use_base_price = Column(Boolean)
    
    ## Relationships
    category = relationship('Category', back_populates='group')
    type = relationship('Type', back_populates='group')

    @classmethod
    def sde_parse(cls, sde_record):
        sde_obj = cls(
            group_id=sde_record.get('groupID'),
            group_name=sde_record.get('name', {}).get('en'),
            category_id=sde_record.get('categoryID'),
            icon_id=sde_record.get('iconID'),
            anchorable=sde_record.get('anchorable'),
            anchored=sde_record.get('anchored'),
            fittable_non_singleton=sde_record.get('fittableNonSingleton'),
            published=sde_record.get('published'),
            use_base_price=sde_record.get('useBasePrice'),
        )
        return sde_obj