from fastapi import FastAPI, Request
from core.model import models
from core.router import user_route, pet_route
from core.db.database import engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel

class BaseResponseModel(BaseModel):
    status_code: int
    detail: str
    
app = FastAPI()

@app.get("/api/v1")
async def pong():
    return {"message": "Hello World!"}

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc):
    error_response = BaseResponseModel(
        status_code=404,
        detail="Not Found"
    )
    return JSONResponse(status_code=404, content=error_response.dict())

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # errors = exc.errors()
    # error_messages = []
    # for error in errors:
    #     error_msg = {
    #         "loc": list(error.get("loc", [])),
    #         "msg": error.get("msg"),
    #         "type": error.get("type"),
    #     }
    #     error_messages.append(error_msg)

    response_data = BaseResponseModel(
        status_code=400,
        detail="Invalid request"
    )
    return JSONResponse(status_code=400, content=response_data.dict())



app.include_router(user_route.router, prefix="/api/v1")
app.include_router(pet_route.router, prefix="/api/v1")

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
    "http://localhost:3003",
    "http://localhost:3004",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(engine)
# user_model.Base.metadata.create_all(engine)
# pet_model.Base.metadata.create_all(engine)