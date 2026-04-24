import os
import aiofiles
import asyncio


async def delete_file(path: str):
    try:
        await asyncio.to_thread(os.remove, path)
    except FileNotFoundError:
        pass


async def create_file(path, file):
    async with aiofiles.open(path, "wb") as buffer:
        while chunk := await file.read(1024 * 1024):  # read 1MB in loop
            await buffer.write(chunk)
        return "Ok"
