from fastapi import FastAPI
from core.config import Settings
from starlette.middleware.cors import CORSMiddleware
from apps.user.routes.user import router as user_router
from core.utils.reponse import Response,RequestValidationError
settings = Settings()
app = FastAPI()

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(user_router, prefix='/api/v1')

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Handle the validation error globally
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    # Return the error as a JSON response with details about the validation error
    errors = []
    for error in exc.errors():
        e= {}
        e['type']=error['type']
        e['loc']=error['loc']
        e['msg']=error['msg']
        if 'ctx' in error.keys():
            e['ctx']=error['ctx']['error']
        

        errors.append(e)
    errors = errors[0] if len(errors)==1 else errors

    return Response(message=errors, success=False,code=422)

# app.include_router(websocket_router)
