from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER as Integer, TINYTEXT as TinyText

from .. import _Base

class Name(_Base):
    __tablename__ = 'itm_Name'
    
    ## Columns
    item_id = Column(Integer(unsigned=True), primary_key=True, autoincrement=False)
    item_name = Column(TinyText)

    @classmethod
    def sde_parse(cls, sde_record):
        sde_obj = cls(
            item_id=sde_record.get('itemID'),
            item_name=sde_record.get('itemName'),
        )
        return sde_obj