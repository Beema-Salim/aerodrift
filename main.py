from ingestion.exposure_detector import find_public_ingress
from ingestion.drift_event import create_drift_events
from remediation.remediation_engine import build_remediation
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

    # Collect current AWS resources
    ingestion_data = collect_all_resources()

    # Get security groups
    security_groups = ingestion_data.get("security_groups", [])

    # Detect public ingress exposures
    exposures = find_public_ingress(security_groups)

    # Convert exposures into AeroDrift events
    drift_events = create_drift_events(exposures)

    return {
        "drift_count": len(drift_events),
        "issues": drift_events
    }

@app.get("/remediation")
def get_remediation():

    # Collect current AWS resources
    ingestion_data = collect_all_resources()

    # Detect public ingress exposures
    security_groups = ingestion_data.get("security_groups", [])
    exposures = find_public_ingress(security_groups)

    # Create drift events
    drift_events = create_drift_events(exposures)

    # Build remediation plans without executing them
    actions = []

    for event in drift_events:
        try:
            remediation_plan = build_remediation(event)

            actions.append({
                "resource_id": event["resource_id"],
                "event_type": event["event_type"],
                "status": "planned",
                "action_type": type(remediation_plan)._name_
            })

        except ValueError:
            continue

    return {
        "status": "planned" if actions else "pending",
        "actions": actions
    }

@app.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"request": request}
    )