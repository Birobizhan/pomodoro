from fastapi import FastAPI, Query, Path
from typing import Annotated
from handlers import routers
app = FastAPI()

for router in routers:
    app.include_router(router)


@app.get('/')
async def get_params():
    return {'message': 'ok'}
