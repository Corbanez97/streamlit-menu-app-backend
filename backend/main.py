from fastapi import FastAPI, Request, HTTPException
from fastapi.security import APIKeyHeader

from backend.config import settings

from backend.api.menu import router as menu_router
from backend.api.users import router as user_router
from backend.api.orders import router as order_router

tags_metadata = [
    {"name": "Menu Items Endpoints", "description": "All about menu items"},
    {"name": "Orders Endpoints", "description": "All about orders and order items"},
    {"name": "Users Endpoints", "description": "All about users"}
]

app = FastAPI(openapi_tags=tags_metadata)

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

@app.middleware("http")
async def api_key_middleware(request: Request, call_next):
    if request.url.path.startswith("/docs") or request.url.path.startswith("/openapi.json"):
        return await call_next(request)
    
    api_key = request.headers.get("Authorization")
    if api_key != f"{settings.API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return await call_next(request)

app.include_router(menu_router)
app.include_router(user_router)
app.include_router(order_router)