from fastapi import APIRouter, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from templates import templates
from src.gemini_ai import translate

router = APIRouter(tags=["translator"])

@router.get("/", response_class=HTMLResponse)
async def view_details(request: Request):
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "reply": "Ashik"}  # Pass the request and data to the template
    )

@router.post("/uploadfile")
async def upload_file(request: Request, file:UploadFile = File(...), language:str = Form(...)):
    content = await file.read()
    source_text = content.decode("utf-8")

    translated_text = translate(source_text,language)

    context = {
        "request" : request,
        "status" : f"File '{file.filename}'",
        "translated_text" : translated_text
    }



    return templates.TemplateResponse("index.html", context)

@router.get("/session-history")
async def session_history(request:Request):
    context = {
        "request" : request,
        "show_history" : True
    }

    return templates.TemplateResponse("index.html", context)
