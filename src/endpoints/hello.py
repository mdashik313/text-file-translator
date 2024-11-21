from fastapi import APIRouter, Body, status, HTTPException, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from fastapi.templating import Jinja2Templates

from fastapi.encoders import jsonable_encoder
from datetime import date, datetime


router = APIRouter(prefix="/api", tags=["translator"])

templates = Jinja2Templates(directory="templates")


@router.get("/", response_description="hello", response_class=HTMLResponse)
async def view_details(request: Response):
    return templates.TemplateResponse(request=request, name="home.html", context={"reply": "Ashik"})