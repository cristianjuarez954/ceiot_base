from ..database import db
from bson import json_util
import json

COLLECTION = "measurements"

async def create_mesurement(mesurement: dict):
    return await db.get_collection(COLLECTION).insert_one(mesurement)

async def get_mesurements():
    return json.loads(json_util.dumps(await db.get_collection(COLLECTION).find().to_list(length=None)))