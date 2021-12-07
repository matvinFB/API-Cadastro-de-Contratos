from fastapi import FastAPI
from fastapi.responses import PlainTextResponse 
from fastapi.exceptions import RequestValidationError

from routes import routes
app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handle(request, exc):
    return PlainTextResponse(status_code=400)


app.include_router(routes.router)
