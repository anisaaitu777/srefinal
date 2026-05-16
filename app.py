import time
import random
from fastapi import FastAPI, HTTPException, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI(title="srefinal API Gateway")

REQUEST_COUNT = Counter('srefinal_requests_total', 'Total count of requests', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Histogram('srefinal_request_latency_seconds', 'Request latency in seconds', ['endpoint'])

@app.middleware("http")
async def monitor_requests(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    latency = time.time() - start_time
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path, http_status=response.status_code).inc()
    REQUEST_LATENCY.labels(endpoint=request.url.path).observe(latency)
    return response

@app.get("/")
def read_root():
    return {"status": "healthy", "project": "srefinal", "message": "Welcome to SRE Final Platform"}

@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)