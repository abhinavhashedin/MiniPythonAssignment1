from database import Base
from sqlalchemy import Column,Integer,String,DateTime,ARRAY,DateTime,func

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)  
    user=Column(String(10))
    key=Column(String(50))
    value=Column(String(50))
    Tags=ARRAY(String(20),as_tuple=False, dimensions=None, zero_indexes=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at=Column(DateTime(timezone=True), default=func.now())

