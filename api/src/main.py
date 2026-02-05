from fastapi import FastAPI, Response, status
from fastapi.responses import HTMLResponse

app = FastAPI(title="MLOps Service")

# TODO 1: Create GET /health that returns JSON like {"status": "ok"}


# TODO 2: Create GET /hello that returns an HTML page using HTMLResponse
