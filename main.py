from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI(title="AeroDrift API")
templates = Jinja2Templates(directory="web/templates")

@app.get("/")
def home():
   return {"message": "Welcome to AeroDrift API"}

@app.get("/topology")
def get_topology():
    return {
        "nodes": [],
        "edges": []
    }

@app.get("/drift")
def get_drift():
    return {
        "drift_count": 0,
        "issues": []
    }

@app.get("/remediation")
def get_remediation():
    return {
        "status": "pending",
        "actions": []
    }

@app.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"request": request}
    )