from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import List

class File(BaseModel):
    translated_file_name: str
    file_path: str
    translated_text: str
    processed_at: str


class SessionSchema(BaseModel):
    session_id: str
    created_at: str
    files_processed: List[File] = []

    class Config:  #JSON example that will display in API documentation
        json_schema_extra = { 
            "example": {
                "session_id": "13948384",
                "created_at": "YYYY-MM-DD HH:MM:SS.ssssss",
                "files_processed": [
                    {
                        "translated_file_name": "example.txt",
                        "file_path": "/files/example.txt",
                        "processed_at": "2024-11-22T08:50:00.000000",
                        "translated_text": "Translated text"
                    },
                    {
                        "translated_file_name": "example.txt",
                        "file_path": "/files/example.txt",
                        "processed_at": "2024-11-22T08:50:00.000000",
                        "translated_text": "Translated text"
                    }
                ]
            }
        }

