from fastapi import FastAPI, Response, status
from fastapi.responses import HTMLResponse

app = FastAPI(title="MLOps Service")

# TODO 1: Create GET /health that returns JSON like {"status": "ok"}
@app.get("/health")
def health():
    return {"status": "ok"}

# TODO 2: Create GET /hello that returns an HTML page using HTMLResponse
@app.head("/health")
def health_head():
    return Response(status_code=status.HTTP_200_OK)

@app.get("/hello", response_class=HTMLResponse)
def hello():
    return """<!doctype html>
    <html>
    <head>Hello!</head>
    <body>
    <p>This page is served by a FastAPI endpoint</p>
    </body>
    </html>
    """