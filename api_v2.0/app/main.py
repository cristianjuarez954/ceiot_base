import logging
from typing import Annotated, List

from contextlib import asynccontextmanager 
from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .crud import devices_crud, mesurements_crud

logger = logging.getLogger('uvicorn.error')

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Generating data in database...")

    await mesurements_crud.create_mesurement({"id": "00", "t": "18", "p": "102000.00"})
    await mesurements_crud.create_mesurement({"id": "00", "t": "19", "p": "102000.00"})
    await mesurements_crud.create_mesurement({"id": "00", "t": "17", "p": "102001.00"})
    await mesurements_crud.create_mesurement({"id": "02", "t": "17", "p": "102002.00"})
    logger.info("mongo measurement database Up")
    try:
        await devices_crud.create_device({"id": "02", "name": "Fake Device 02", "key": "234567"})
        await devices_crud.create_device({"id": "00", "name": "Fake Device 00", "key": "123456"})
        logger.info("sql device database up")
    except HTTPException as e:
        logger.warning("Ya existian los dispositivos")

    yield

app = FastAPI(lifespan=lifespan)

app.frontend("/", directory="spa/static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/measurement",response_model=str)
async def create_mesurement(id: Annotated[str, Form()], key: Annotated[str, Form()], t: Annotated[str, Form()], p: Annotated[str, Form()]):
    logger.info("device id: %s key: %s temperature: %s pressure: %s",id,key,t,p)
    db_obj = await mesurements_crud.create_mesurement({"id": id, "t": t, "p": p}) 
    return "received measurement into {}".format(db_obj.inserted_id)

@app.post("/device",response_model=str)
async def create_device(id: Annotated[str, Form()], name: Annotated[str, Form()], key: Annotated[str, Form()]):
    logger.info("device id: %s name: %s key: %s",id,name,key)
    await devices_crud.create_device({"id": id, "name": name, "key": key}) 
    return "received new device"

@app.get("/web/device",response_model=str)
async def get_web_devices():
    logger.info("Getting devices...")
    html_devices=["<tr><td><a href=/web/device/{}>{}</a></td><td>{}</td><td>{}</td></tr>".format(device["id"],device["id"],device["name"],device["key"]) for device in devices]
    return """
    <html>
		<head><title>Sensores</title></head>
        <body>
            <table border=\"1\">
                <tr><th>id</th><th>name</th><th>key</th></tr>
                {}
            </table>
        </body>"
	</html>""".format(html_devices)

@app.get("/web/device/{id}",response_model=str)
async def get_web_device_by_id(id):
    logger.info("Getting device %s",id)
    device =await devices_crud.get_device(id) 
    return """
    <html>
        <head><title>Sensor {}</title></head>
        <body>
            <h1>{}</h1>
            id  : {}<br/>
            Key : {}
        </body>
    </html>""".format(device["name"],device["name"],device["id"],device["key"])

@app.get("/term/device/{id}",response_model=str)
async def get_term_device_by_id(id):
    logger.info("Getting device %s",id)
    device =await devices_crud.get_device(id) 
    return """
        Device name \33[31m {} \33[0m
        id   \33[32m {} \33[0m
        key  \33[33m {} \33[0m
    """.format(device["name"],device["id"],device["key"])


@app.get("/measurement",response_model=List[dict])
async def get_mesurements():
    logger.info("Getting measurements...")
    return await mesurements_crud.get_mesurements()

@app.get("/device",response_model=List[dict])
async def get_devices():
    logger.info("Getting devices...")
    return await devices_crud.get_devices()

