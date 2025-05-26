from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def read_root():
    return JSONResponse(content={"message": "Folio API is running"})
