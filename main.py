from fastapi import FastAPI, HTTPException
from supabase import create_client
from dotenv import load_dotenv
import os
from pydantic import BaseModel

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

class AuthRequest(BaseModel):
    email: str
    password: str

@app.get("/")
def root():
    return {
        "message": "FlyRank Auth API is running"
    }
@app.post("/auth/signup", status_code=201)
def signup(data: AuthRequest):

    if not data.email or not data.password:
        raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )

    try:
        response = supabase.auth.sign_up({
            "email": data.email,
            "password": data.password
        })

        return response.user

    except Exception as e :
        raise HTTPException(
             status_code=400,
             detail=str(e)
        )
@app.post("/auth/login")
def login(data: AuthRequest):

    if not data.email or not data.password:
        raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )

    try:
        response = supabase.auth.sign_in_with_password({
            "email": data.email,
            "password": data.password
        })

        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token
        }

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid login credentials"
        )