import aiofiles
import os

async def save_upload_file(file, filename: str):
    async with aiofiles.open(filename, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

def remove_file(path: str):
    if os.path.exists(path):
        os.remove(path)
