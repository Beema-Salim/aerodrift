from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
import requests

console = Console()
api_error = None

API_BASE_URL = "http://127.0.0.1:8000"

TOPOLOGY_API_URL = f"{API_BASE_URL}/topology"
DRIFT_API_URL = f"{API_BASE_URL}/drift"
REMEDIATION_API_URL = f"{API_BASE_URL}/remediation"

environment_data = {
    "name": "Development",
    "region": "ap-south-1",
    "last_updated": "Week 1 Mock Run"
}

title = Text("AeroDrift CLI Dashboard", style="bold cyan")
subtitle = Text("Cloud Infrastructure Monitoring", style="dim")

console.print(title, justify="center")
console.print(subtitle, justify="center")

dashboard_data = {
    "topology": {
        "nodes": 4,
        "edges": 3
    },
    "drift": {
        "drift_count": 0,
        "issues": 0
    },
    "remediation": {
        "status": "pending",
        "actions": 0
    }
}

def get_dashboard_data(api_data=None):
    required_sections = {"topology", "drift", "remediation"}

    if isinstance(api_data, dict) and required_sections.issubset(api_data):
        return api_data, "API Data"

    return dashboard_data, "Mock Data"

def get_data_source(api_data):
    if api_data:
        return "API Connected"

    return "API Unavailable - Using Mock Data"


def create_topology_panel(data):
    return Panel(
        f"[bold]Nodes:[/bold] {data['nodes']}\n"
        f"[bold]Edges:[/bold] {data['edges']}",
        title="Topology",
        border_style="blue"
    )


def create_drift_panel(data):
    return Panel(
        f"[bold]Drift Count:[/bold] {data['drift_count']}\n"
        f"[bold]Issues:[/bold] {data['issues']}",
        title="Drift",
        border_style="yellow"
    )


def create_remediation_panel(data):
    return Panel(
        f"[bold]Status:[/bold] {data['status']}\n"
        f"[bold]Actions:[/bold] {data['actions']}",
        title="Remediation",
        border_style="green"
    )

def get_topology_from_api():
    api_data = fetch_api_data(TOPOLOGY_API_URL)

    if validate_api_data(api_data, ["nodes", "edges"]):
        return api_data

    return dashboard_data["topology"]

def get_drift_from_api():
    api_data = fetch_api_data(DRIFT_API_URL)

    if validate_api_data(api_data, ["drift_count", "issues"]):
        return api_data

    return dashboard_data["drift"]

def get_remediation_from_api():
    api_data = fetch_api_data(REMEDIATION_API_URL)

    if validate_api_data(api_data, ["status", "actions"]):
        return api_data

    return dashboard_data["remediation"]

def fetch_api_data(url):
    global api_error

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        data = response.json()

        if isinstance(data, dict):
            api_error = None
            return data

        api_error = "Invalid API response"
        return None

    except requests.Timeout:
        api_error = "API request timed out"
        return None

    except (requests.RequestException, ValueError):
        api_error = "API unavailable"
        return None

def validate_api_data(data, required_fields):
    if not isinstance(data, dict):
        return False

    return all(field in data for field in required_fields)

def test_dashboard_api_data():
    topology = get_topology_from_api()
    drift = get_drift_from_api()
    remediation = get_remediation_from_api()

    assert "nodes" in topology
    assert "edges" in topology
    assert isinstance(topology["nodes"], int)
    assert isinstance(topology["edges"], int)

    assert "drift_count" in drift
    assert "issues" in drift
    assert isinstance(drift["drift_count"], int)
    assert isinstance(drift["issues"], list)

    assert "status" in remediation
    assert "actions" in remediation
    assert isinstance(remediation["status"], str)
    assert isinstance(remediation["actions"], (int, list))

    print("Dashboard API integration test passed.")

topology_data = get_topology_from_api()
drift_data = get_drift_from_api()
remediation_data = get_remediation_from_api()

refresh_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

data, data_source = get_dashboard_data({
    "topology": topology_data,
    "drift": drift_data,
    "remediation": remediation_data
})

if api_error:
    connection_status = api_error
else:
    connection_status = get_data_source(topology_data)

source = "Mock" if api_error else "API"

endpoint_status = (
    f"Topology: {source} | "
    f"Drift: {source} | "
    f"Remediation: {source}"
)

topology_panel = create_topology_panel(topology_data)

drift_panel = create_drift_panel(drift_data)

remediation_panel = create_remediation_panel(remediation_data)

summary_panel = Panel(
    f"Cloud State: {data_source}\n"
    f"API Status: {connection_status}\n"
    f"Endpoints: {endpoint_status}\n"
    f"Environment: {environment_data['name']}\n"
    f"Region: {environment_data['region']}\n"
    f"Last Updated: {environment_data['last_updated']}\n"
    f"Data Refreshed: {refresh_time}\n"
    f"Resources: {topology_data['nodes']}\n"
    f"Status: Ready",
    title="System Status",
    border_style="magenta"
)

console.print(
    Columns([
        topology_panel,
        drift_panel,
        remediation_panel
    ])
)
console.print(summary_panel)

test_dashboard_api_data()