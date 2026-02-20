from fastapi import FastAPI, HTTPException, Depends, Header
import secrets

app = FastAPI()

api_keys = {}

def generate_api_key():
    return secrets.token_hex(32)

@app.post("/generate-key")
def create_key(user: str):
    key = generate_api_key()
    api_keys[key] = user
    return {"api_key": key}

def verify_key(x_api_key: str = Header(...)):
    if x_api_key not in api_keys:
        raise HTTPException(status_code=401, detail="Invalid API key")

@app.get("/protected")
def protected_route(dep=Depends(verify_key)):
    return {"message": "Access granted "}
