from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import datetime
from schemas.partner import PartnerCreate
from database.connection import engine, Base, get_db
from database import models
from services.validator import run_validation_checks
from services.report_generator import generate_health_report
from routers import auth
from routers.auth import get_current_user
from database.models import User

start_time = datetime.datetime.utcnow()


app=FastAPI()
app.include_router(auth.router)
@app.on_event("startup")
def startup():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created!")
    
    
@app.get('/')
def home():
    return {'message':'Hello User'}

@app.get('/status')
def status():
    return {'status':'healthy', 'uptime':datetime.datetime.utcnow()-start_time, 'version':'1.0.0'}


@app.get('/info')
def info():
    return {'project':'gTech Ad manager','description':'Sophisticated app for Ad publishers','tech stack':'Python, FastAPi and much more','author':'sathwik'}


@app.post('/partners')
def create_partner(partner: PartnerCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_partner = models.Partner(
        company_name=partner.company_name,
        company_url=partner.company_url,
        ad_platform=partner.ad_platform,
        api_endpoint=partner.api_endpoint,
        auth_method=partner.auth_method
    )
    db.add(new_partner)
    db.commit()
    db.refresh(new_partner)
    return new_partner

#To get all partners
@app.get('/partners')
def get_partners(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    partners = db.query(models.Partner).all()  
    return partners
    
    
#To get one partner    
@app.get('/partners/{partner_id}')
def get_partner(partner_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    partner = db.query(models.Partner).filter(models.Partner.id == partner_id).first()
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    return partner


    
@app.post('/validate/{partner_id}')
async def validate_partner(partner_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    partner = db.query(models.Partner).filter(models.Partner.id == partner_id).first()
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    

    checks = await run_validation_checks(partner.api_endpoint, partner.auth_method, partner.ad_platform)
    report = generate_health_report(checks)
    return report