import os
import asyncio
import aiofiles
from uuid import uuid4
from fastapi import UploadFile
from ..error import FileSaveError, FileDeleteError

async def save_pdf_file(file: UploadFile) -> str:
    """Save uploaded PDF file with UUID prefix"""
    try:
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, f"{uuid4()}_{file.filename}")
        async with aiofiles.open(file_path, "wb") as buffer:
            await file.seek(0)
            while content := await file.read(64 * 1024):
                await buffer.write(content)
        return file_path
    except Exception as e:
        raise FileSaveError(f"Failed to save file: {str(e)}") from e

async def remove_file(file_path: str):
    """Remove a file from the filesystem"""
    if os.path.exists(file_path):
        try:
            await asyncio.get_event_loop().run_in_executor(None, os.remove, file_path)
        except Exception as e:
            raise FileDeleteError(f"Error deleting file {file_path}") from e