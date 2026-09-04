from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from ingestion.async_collector import collect_all_resources_async
from ingestion.exposure_detector import find_public_ingress
from ingestion.drift_event import create_drift_events
from remediation.remediation_engine import build_remediation
from topology.graph_builder import GraphBuilder
from ingestion.topology_adapter import normalize_resources


app = FastAPI(title="AeroDrift API")

templates = Jinja2Templates(directory="web/templates")

app.mount("/static", StaticFiles(directory="web/static"), name="static")


@app.get("/")
def home():
    return {"message": "Welcome to AeroDrift API"}


@app.get("/topology")
async def get_topology():
    data = await collect_all_resources_async()

    resources = normalize_resources(data)

    builder = GraphBuilder()
    graph = builder.build(resources)

    nodes = [
        {
            "id": node_id,
            **attributes
        }
        for node_id, attributes in graph.nodes(data=True)
    ]

    edges = [
        {
            "source": source,
            "target": target,
            **attributes
        }
        for source, target, attributes in graph.edges(data=True)
    ]

    return {
        "nodes": nodes,
        "edges": edges
    }


@app.get("/drift")
async def get_drift():
    data = await collect_all_resources_async()

    exposures = find_public_ingress(data["security_groups"])
    events = create_drift_events(exposures)

    return {
        "drift_count": len(events),
        "issues": events
    }


@app.get("/remediation")
async def get_remediation():
    data = await collect_all_resources_async()

    exposures = find_public_ingress(data["security_groups"])
    drift_events = create_drift_events(exposures)

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
        "remediation_count": len(actions),
        "actions": actions
    }


@app.get("/drift-demo")
def get_drift_demo():
    """
    Simulated critical drift for dashboard demonstration.
    This endpoint does not modify any AWS resource.
    """
    demo_event = {
        "event_type": "PUBLIC_INGRESS",
        "resource_type": "SECURITY_GROUP",
        "resource_id": "sg-demo-public",
        "severity": "CRITICAL",
        "cidr": "0.0.0.0/0",
        "protocol": "tcp",
        "from_port": 22,
        "to_port": 22,
    }

    return {
        "demo": True,
        "drift_count": 1,
        "issues": [demo_event],
    }


@app.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"request": request}
    )


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AeroDrift API"
    }