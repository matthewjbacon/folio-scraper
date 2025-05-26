from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Folio MVP is live!"}
