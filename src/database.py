import motor.motor_asyncio  #motor is asynchronous python driver for MongoDB
from src.models.session import  File, SessionSchema
import os
import dotenv
dotenv.load_dotenv()


client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_CONNECTION_URI"))
database = client.sessionDB
session_history = database.get_collection("session_history")
print("Connected to the MongoDB database!")

async def add_translated_file(session_data: dict, session_id: str):
    task = session_data[session_id]
    existing_session = await session_history.find_one({"session_id": session_id})
    if not existing_session:
        #If the session doesn't exist, create one
        session_doc = SessionSchema(
            session_id=session_id,
            created_at=task["created_at"],
            files_processed=[]
        )
        await session_history.insert_one(session_doc.dict())
        # return session_data.dict()

    #Add the file details to the session (either new or existing)
    file_data = File(
        translated_file_name=task["translated_file_name"],
        file_path=task["file_path"],
        translated_text=task["translated_text"],
        processed_at=task["processed_at"]
    )

    #Update the session document in MongoDB
    await session_history.update_one(
        {"session_id": session_id},
        {"$push": {"files_processed": file_data.dict()}}
    )

    return file_data.dict()

async def get_history_by_session_id(session_id: str):
    results = await session_history.find_one({"session_id": session_id})
    return results

async def get_all_history():
    sessions = []
    async for session in session_history.find():
        sessions.append(session) 
    return sessions