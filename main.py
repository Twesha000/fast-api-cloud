from fastapi import FastAPI, HTTPException # pyright: ignore[reportMissingImports]
from pydantic import BaseModel # pyright: ignore[reportMissingImports]
from typing import List, Dict, Any, Optional # pyright: ignore[reportMissingImports]
import mysql.connector # pyright: ignore[reportMissingImports]

class Item(BaseModel):
    input: str
    params: str | None = None
    output: str
    time: str
    
app = FastAPI()

# --- Database Connection ---
def get_connection():
    return mysql.connector.connect(
        host="sql12.freesqldatabase.com",
        user="sql12791047",
        password="X7v7jUxfNV",
        database="sql12791047"
    )


# --- Upload Endpoint ---
@app.post("/upload-payload", tags=['Up Load'])
def upload_payload(payload: Dict[str, Any]):
    data = payload
    con = get_connection()
    cursor = con.cursor()

    try:
        cursor.execute("""
            INSERT INTO payload (input, params, output, time)
            VALUES (%s, %s, %s, %s)
        """, (
            data.get("input"),
            data.get("params"),
            data.get("output"),
            data.get("time_of_execution")
        ))

        con.commit()
        return {"message": "Payload inserted successfully"}

    except Exception as e:
        con.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        con.close()
        return Item


if __name__ == "__main__":
    import uvicorn # pyright: ignore[reportMissingImports]
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

