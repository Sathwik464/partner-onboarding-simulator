from sqlalchemy import Column, Integer, String, DateTime, Sequence
from datetime import datetime
from database.connection import Base

#This is Partner Model which is used to store the partner details in the database. Equivalent to a table in DB
class Partner(Base):
    __tablename__ = 'partners'
    id = Column(Integer, Sequence('partner_id_seq'), primary_key=True)
    company_name = Column(String(100), unique=False, index=True, nullable=False)
    company_url = Column(String(200), nullable=False)
    ad_platform = Column(String(100), nullable=False)
    api_endpoint = Column(String(200), nullable=False)
    auth_method = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
#This is User Model which is used to store user details in the database for JWT purposes
class User(Base):
    __tablename__= 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key = True)
    email = Column(String(100), unique = True, nullable = False)
    password = Column(String(200), nullable = False)
    created_at = Column(DateTime, default = datetime.utcnow)
    