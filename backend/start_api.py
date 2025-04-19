import traceback

import uvicorn
from fastapi import FastAPI, Request
from loguru import logger
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import PlainTextResponse, RedirectResponse

from api.api_endpoints import router

app = FastAPI(
    title="Gallery Rush Game - Backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    """
    This will present errors in a much easier way to understand what happened.

    :param request:
    :param exc:
    :return:
    """
    logger.error(f"Request failed: {exc}")
    traceback_str = "".join(traceback.format_tb(exc.__traceback__))
    logger.error(f"Traceback: {traceback_str}")
    return PlainTextResponse(str(exc), status_code=500)

@app.get("/", response_class=RedirectResponse)
def read_root(request: Request):
    """
    This will redirect the user to the swagger page, explaining the different endpoints

    :param request:
    :return:
    """
    base_url = request.url.scheme + "://" + request.url.netloc
    return RedirectResponse(url=base_url + "/docs")

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )
