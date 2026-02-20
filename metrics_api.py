from fastapi import FastAPI, Request
import time

app = FastAPI()

total_requests = 0
start_time = time.time()

@app.middleware("http")
async def count_requests(request: Request, call_next):
    global total_requests
    total_requests += 1
    response = await call_next(request)
    return response

@app.get("/")
def home():
    return {"message": "API running"}

@app.get("/metrics")
def metrics():
    uptime = time.time() - start_time
    return {
        "total_requests": total_requests,
        "uptime_seconds": round(uptime, 2)
    }
