import asyncio
import base64

import cv2
from fastapi import FastAPI, WebSocket, Request, Response

from HighKnees import process_image
from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate
from operations.router import router as router_operation
from pages.router import router as router_pages

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


app = FastAPI(
    title="Fitness App"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("live_pose.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        img, fps, repetitions_count = process_image()

        _, img_encoded = cv2.imencode('.jpg', img)
        img_base64 = base64.b64encode(img_encoded.tobytes()).decode('utf-8')

        await websocket.send_json({
            'image': img_base64,
            'fps': int(fps),
            'jumps': repetitions_count
        })

        await asyncio.sleep(0.1)


app.include_router(router_operation)
app.include_router(router_pages)
