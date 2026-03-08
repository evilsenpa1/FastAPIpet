import os
from fastapi import HTTPException
import aiofiles

def delete_file(path: str):
    if os.path.exists(path):
        os.remove(path)
    else:
        raise HTTPException(status_code=404, detail="File not found")


async def create_file(path, file):
    async with aiofiles.open(path, "wb") as buffer:
        while chunk := await file.read(1024 * 1024):  # read 1MB in loop
            await buffer.write(chunk)
        return "Ok"
