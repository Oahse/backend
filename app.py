from fastapi import FastAPI
from src.controllers.user_controller import router as user_router
from src.controllers.websocket import router as websocket_router

app = FastAPI()

register_routers(app)
app.include_router(websocket_router)
