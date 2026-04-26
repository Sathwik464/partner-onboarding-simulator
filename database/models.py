from sqlalchemy import Column, Integer, String, DateTime, Sequence
from datetime import datetime
from database.connection import Base

class Partner(Base):
    __tablename__ = 'partners'
    id = Column(Integer, Sequence('partner_id_seq'), primary_key=True)
    company_name = Column(String(100), unique=False, index=True, nullable=False)
    company_url = Column(String(200), nullable=False)
    ad_platform = Column(String(100), nullable=False)
    api_endpoint = Column(String(200), nullable=False)
    auth_method = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    