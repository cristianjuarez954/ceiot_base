import logging
from typing import Annotated, List


from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware

from .crud import devices_crud, mesurements_crud

app = FastAPI()

app.frontend("/", directory="spa/static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger('uvicorn.error')

@app.post("/measurement",response_model=str)
async def create_mesurement(id: Annotated[str, Form()], key: Annotated[str, Form()], t: Annotated[str, Form()], p: Annotated[str, Form()]):
    logger.info("device id: {} key: {} temperature: {} pressure: {}",id,key,t,p)
    db_obj = await mesurements_crud.create_mesurement({id: id, t: t, p: p}) 
    return "received measurement into {}".format(db_obj.inserted_id)

@app.post("/device",response_model=str)
async def create_device(id: Annotated[str, Form()], name: Annotated[str, Form()], key: Annotated[str, Form()]):
    logger.info("device id: {} name: {} key: {}",id,name,key)
    await devices_crud.create_device({id: id, name: name, key: key}) 
    return "received new device"

@app.get("/web/device",response_model=str)
async def get_web_devices(id: Annotated[str, Form()], name: Annotated[str, Form()], key: Annotated[str, Form()]):
    logger.info("Getting devices...")
    devices =await devices_crud.create_device({id: id, name: name, key: key}) 
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
    logger.info("Getting device {}",id)
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
    logger.info("Getting device {}",id)
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

