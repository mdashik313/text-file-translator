import uvicorn
from fastapi import FastAPI
import pathlib
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routes.api import router as api_router

app = FastAPI()
BASE_DIR = pathlib.Path(__file__).parent
templates = Jinja2Templates(directory=[BASE_DIR / "templates",])
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
