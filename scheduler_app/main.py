from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from scheduler_app.routes import *

app = FastAPI()

# API Doc
app = FastAPI(
    title="Scheduler",
    description="This is a scheduler project",
    version="1.0.0",
)


# Error
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    # print(f"OMG! An HTTP error!: {repr(exc)}")
    # Add error logger here loguru
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"},
    )


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
# app.include_router(
#     schedule.router,
#     prefix="/error",
#     tags=["Error"],
# )
#
# app.include_router(
#     conversion.router,
#     prefix="/conversion",
#     tags=["Conversion"],
# )
