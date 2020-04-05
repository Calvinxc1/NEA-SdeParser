from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER as Integer, TINYTEXT as TinyText, BOOLEAN as Boolean, TEXT as Text
from sqlalchemy.orm import relationship

from .. import _Base

class MarketGroup(_Base):
    __tablename__ = 'inv_MarketGroup'
    
    ## Columns
    market_group_id = Column(Integer(unsigned=True), primary_key=True, autoincrement=False)
    market_group_name = Column(TinyText)
    market_group_desc = Column(Text)
    parent_group_id = Column(Integer(unsigned=True), ForeignKey('inv_MarketGroup.market_group_id'))
    icon_id = Column(Integer(unsigned=True))
    has_types = Column(Boolean)
    
    ## Relationships
    parent_group = relationship('MarketGroup', remote_side=[market_group_id])
    type = relationship('Type')

    @classmethod
    def sde_parse(cls, sde_record):
        try:
            sde_obj = cls(
                market_group_id=sde_record.get('marketGroupID'),
                market_group_name=sde_record.get('nameID', {}).get('en'),
                market_group_desc=sde_record.get('descriptionID', {}).get('en'),
                parent_group_id=sde_record.get('parentGroupID'),
                icon_id=sde_record.get('iconID'),
                has_types=sde_record.get('hasTypes'),
            )
        except Exception as e:
            print(sde_record)
            raise Exception(e)
        return sde_obj