from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # Chef, Employee, Customer

class InitializationFlag(Base):
    __tablename__ = 'initialization_flag'

    id = Column(Integer, primary_key=True)
    initialized = Column(Boolean, default=False)

# Create tables
engine = create_engine('sqlite:///restaurant.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Check if the initialization has already been performed
initialization_done = session.query(InitializationFlag).first()

if not initialization_done: 

    # Create initial users
    chef_user = User(username='chef', password='chef_password', role='Chef')
    employee_user = User(username='employee', password='employee_password', role='Employee')
    customer_user = User(username='customer', password='customer_password', role='Customer')
    session.add_all([chef_user, employee_user, customer_user])

    if not initialization_done:
        initialization_flag = InitializationFlag()
        session.add(initialization_flag)
    else:
        initialization_done.initialized = True

    session.commit()
else:
    print(f"Initialization Already Performed")

session.close()