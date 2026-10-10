from fastapi import HTTPException

from ..database import db
from bson import json_util
import json

COLLECTION = "devices"

async def create_device(device: dict):
    old_device = await db.get_collection(COLLECTION).find_one({"id": device["id"]})
    if not old_device: return await db.get_collection(COLLECTION).insert_one(device)
    raise HTTPException(status_code=400, detail="Device already exists")

async def get_devices():
    return json.loads(json_util.dumps(await db.get_collection(COLLECTION).find({}).to_list(length=None)))

async def get_device(id: str):
    device = await db.get_collection(COLLECTION).find_one({"id": id})
    if not device: raise HTTPException(status_code=404, detail="Device not found")
    return json.loads(json_util.dumps(device))