from fastapi import FastAPI

app = FastAPI(title="AeroDrift API")


@app.get("/")
def home():
   return {"message": "Welcome to AeroDrift API"}

