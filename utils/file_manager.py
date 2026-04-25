import os
import logging
import aiofiles
import asyncio
from pathlib import Path

logger = logging.getLogger(__name__)

UPLOAD_DIR = Path("uploads").resolve()


async def delete_file(path: str) -> None:
    safe_path = Path(path).resolve()
    if not str(safe_path).startswith(str(UPLOAD_DIR)):
        logger.error("Path traversal attempt blocked: %s", path)
        raise ValueError(f"File path is outside upload directory: {path}")
    try:
        await asyncio.to_thread(os.remove, safe_path)
    except FileNotFoundError:
        pass
    except OSError as e:
        logger.warning("Could not delete file %s: %s", path, e)


async def create_file(path, file):
    async with aiofiles.open(path, "wb") as buffer:
        while chunk := await file.read(1024 * 1024):  # read 1MB in loop
            await buffer.write(chunk)
        return "Ok"
