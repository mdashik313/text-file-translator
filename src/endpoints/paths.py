from fastapi import APIRouter, Request, UploadFile, File, Form, WebSocket, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse
from templates import templates
from src.gemini_ai import translate
import time
import asyncio
import uuid
import os
from datetime import date, datetime
from src.database import *


router = APIRouter(tags=["translator"])
active_tasks = {}
BASE_DIR =  os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UPLOAD_DIR = os.path.join(BASE_DIR, "results")

#Ensure the directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Background task processing function
async def translate_in_background(
    session_id: str, 
    source_text: str, 
    target_language: str, 
    file_name: str,
    task_complete_event: asyncio.Event  # asyncio event to notify websocket when tranlataion done
):

    translated_text = await translate(source_text, target_language)
    processed_at = datetime.now()
    processed_at = processed_at.isoformat(sep=" ", timespec="seconds")
    unique_filename = f"{uuid.uuid4()}_{file_name}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)


    # Update task status
    active_tasks[session_id].update({
        "status": "completed",
        "translated_text": translated_text,
        "file_path": file_path,
        "translated_file_name":  unique_filename,
        "processed_at": processed_at
    })

    #Notify websocket that task is complete
    task_complete_event.set() 

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html", 
        {"request": request}  # Pass the request and data to the template
    )


@router.post("/uploadfile")
async def upload_file(
    request: Request,   
    file:UploadFile = File, 
    language:str = Form(...), 
    session_id: str = Form(...),
    created_at: str = Form(...)
):
    content = await file.read()
    source_text = content.decode("utf-8")
    target_language = language
    file_name = file.filename

    # Store session data in shared dictionary
    active_tasks[session_id] = {
        "status": "processing",
        "source_text": source_text,
        "target_language": target_language,
        "file_name": file_name,
        "created_at": created_at
    }

    context = {
        "request" : request,
    }

    return HTMLResponse("")

@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()

    #Retrieve session data
    task = active_tasks[session_id]
    
    #Step 1: Notify "File received"
    await websocket.send_text("Received")
    time.sleep(2)

    source_text = task["source_text"]
    target_language = task["target_language"]
    file_name = task["file_name"]
    task_complete_event = asyncio.Event() 


    #Step 2: Notify "Translating"
    await websocket.send_text("Translating...")
    time.sleep(2)

    asyncio.create_task(
        translate_in_background(
            session_id, source_text, target_language, file_name, task_complete_event
        )
    )

    await task_complete_event.wait()

    #Notify translation complete and send the download link
    translated_file_path = task["file_path"]
    translated_file_name = task["translated_file_name"]
    translated_text = task["translated_text"]
    download_link = f"http://localhost:8000/download/{translated_file_name}/{translated_text}"

    await websocket.send_text(f"Translation complete! Download your file here: {download_link}")

    #Save the file to database
    response = await add_translated_file(active_tasks, session_id)
    
    # delete temporary session data
    del active_tasks[session_id]

    await websocket.close()

@router.get("/download/{file_name}/{translated_text}", response_class=FileResponse)
async def download_file(file_name: str, background_tasks: BackgroundTasks, translated_text : str):
    file_path = os.path.join(UPLOAD_DIR, file_name)

    # Save the file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(translated_text)

    # after downloading, delete the file form server
    background_tasks.add_task(os.remove, file_path)
    return FileResponse(path=file_path, media_type="application/octet-stream", filename=file_name, background=background_tasks)


@router.get("/history/{session_id}", response_class=FileResponse)
async def session_history(request: Request, session_id: str):
    result = await get_history_by_session_id(session_id)
    files = None
    show_history = False

    if result:
        files = result["files_processed"]
        show_history = True

    context = {
        "request" : request,
        "files" : files,
        "show_history" : show_history,
        "page_title" : "Session History"
    }

    return templates.TemplateResponse(
        "history.html",
        context
    )

@router.get("/history", response_class=FileResponse)
async def all_history(request: Request):
    sessions = await get_all_history()
    all_files = []
    show_history = False

    if sessions:
        show_history = True

    # print(sessions)
    for session in sessions:
        for file in session["files_processed"]:
            all_files.append(file)

    context = {
        "request" : request,
        "files" : all_files,
        "show_history" : show_history,
        "page_title" : "All History"
    }

    return templates.TemplateResponse(
        "history.html",
        context
    )