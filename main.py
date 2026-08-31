from topology.graph_builder import GraphBuilder
from ingestion.topology_adapter import normalize_resources
from ingestion.resource_collector import collect_all_resources
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="AeroDrift API")
templates = Jinja2Templates(directory="web/templates")

app.mount("/static", StaticFiles(directory="web/static"), name="static")

@app.get("/")
def home():
   return {"message": "Welcome to AeroDrift API"}

@app.get("/topology")
def get_topology():

    # Collect real AWS resources
    ingestion_data = collect_all_resources()

    # Convert ingestion data to topology format
    resources = normalize_resources(ingestion_data)

    # Build topology graph
    builder = GraphBuilder()
    builder.build(resources)

    # Convert graph to dictionary
    topology = builder.to_dict()

    return {
        "nodes": len(topology["nodes"]),
        "edges": len(topology["edges"])
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