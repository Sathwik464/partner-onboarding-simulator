from pydantic import BaseModel
from typing import Literal

class PartnerCreate(BaseModel):
    company_name:str
    company_url:str
    ad_platform:Literal['GoogleAdManager', 'AdSense', 'AdMob']
    api_endpoint:str
    auth_method:Literal['OAuth', 'JWT','APIKey']
    
    

    
    
    
    