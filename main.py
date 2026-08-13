from fastapi import FastAPI

app = FastAPI(title="AeroDrift API")


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
