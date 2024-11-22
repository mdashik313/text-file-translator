import motor.motor_asyncio  #motor is asynchronous python driver for MongoDB
from src.models.session import  File, SessionSchema


MONGO_DETAILS = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.sessionDB
session_history = database.get_collection("session_history")

async def add_translated_file(session_data: dict, session_id: str):
    task = session_data[session_id]
    existing_session = await session_history.find_one({"session_id": session_id})
    if not existing_session:
        #If the session doesn't exist, create one
        session_data = SessionSchema(
            session_id=session_id,
            created_at=task["created_at"],
            files_processed=[]
        )
        await session_history.insert_one(session_data.dict())
        return session_data.dict()

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

async def get_translated_files(session_id: str):
    results = await session_history.find_one({"session_id": session_id})
    return results