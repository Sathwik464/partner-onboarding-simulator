from pydantic import BaseModel

# For registration
class UserRegister(BaseModel):
    email: str
    password: str

# For login — same fields, different name
class UserLogin(BaseModel):
    email: str
    password: str

# For token response — what server sends back after login
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    

    