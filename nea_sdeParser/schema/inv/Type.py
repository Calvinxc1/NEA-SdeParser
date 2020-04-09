from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER as Integer, TINYTEXT as TinyText, BOOLEAN as Boolean, DOUBLE as Double, TEXT as Text, FLOAT as Float
from sqlalchemy.orm import relationship

from .. import _Base

class Type(_Base):
    __tablename__ = 'inv_Type'
    
    ## Columns
    type_id = Column(Integer(unsigned=True), primary_key=True, autoincrement=False)
    type_name = Column(TinyText)
    type_desc = Column(Text)
    group_id = Column(Integer(unsigned=True), ForeignKey('inv_Group.group_id'))
    market_group_id = Column(Integer(unsigned=True), ForeignKey('inv_MarketGroup.market_group_id'))
    faction_id = Column(Integer(unsigned=True))
    graphic_id = Column(Integer(unsigned=True))
    icon_id = Column(Integer(unsigned=True))
    meta_group_id = Column(Integer(unsigned=True))
    sound_id = Column(Integer(unsigned=True))
    race_id = Column(Integer(unsigned=True))
    variation_parent_type_id = Column(Integer(unsigned=True))
    base_price = Column(Float(unsigned=True))
    capacity = Column(Float(unsigned=True))
    mass = Column(Double(unsigned=True))
    portion_size = Column(Integer(unsigned=True))
    published = Column(Boolean)
    radius = Column(Float(unsigned=True))
    volume = Column(Float(unsigned=True))
    sof_faction_name = Column(TinyText)
    sof_material_set_id = Column(Integer(unsigned=True))
    
    ## Relationships
    group = relationship('Group', back_populates='type')
    market_group = relationship('MarketGroup', back_populates='type')

    @classmethod
    def sde_parse(cls, sde_record):
        sde_obj = cls(
            type_id=sde_record.get('typeID'),
            type_name=sde_record.get('name', {}).get('en'),
            type_desc=sde_record.get('description', {}).get('en'),
            group_id=sde_record.get('groupID'),
            market_group_id=sde_record.get('marketGroupID'),
            faction_id=sde_record.get('factionID'),
            graphic_id=sde_record.get('graphicID'),
            icon_id=sde_record.get('iconID'),
            meta_group_id=sde_record.get('metaGroupID'),
            sound_id=sde_record.get('soundID'),
            race_id=sde_record.get('raceID'),
            variation_parent_type_id=sde_record.get('variationParentTypeID'),
            base_price=sde_record.get('basePrice'),
            capacity=sde_record.get('capacity'),
            mass=sde_record.get('mass'),
            portion_size=sde_record.get('portionSize'),
            published=sde_record.get('published'),
            radius=sde_record.get('radius'),
            volume=sde_record.get('volume'),
            sof_faction_name=sde_record.get('sofFactionName'),
            sof_material_set_id=sde_record.get('sofMaterialSetID'),
        )
        return sde_obj