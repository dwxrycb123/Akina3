import os
import json
import aiofiles

async def get_json(filepath):
    async with aiofiles.open(filepath, mode='r', encoding='UTF-8') as f:
        s = await f.read()
        return json.loads(s)

async def save_json(filepath, data):
    s = json.dumps(data)
    async with aiofiles.open(filepath, mode="w", encoding="UTF-8") as f:
        await f.write(s)