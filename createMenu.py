
from sqlalchemy import create_engine, Column, Integer, String
import init 
class MenuItem(init.Base):
    __tablename__ = 'menu_items'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    price = Column(Integer, nullable=False)

# Create tables
init.Base.metadata.create_all(init.engine)
