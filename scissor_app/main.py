from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.url_routes import url_router
from .routes.user_routes import user_router
from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


"""
    The function returns a welcome message confirming that the Scissor app is running.
    :return: The string "Welcome to the Scissor app :)" is being returned.
"""


@app.get("/", tags=["Health Check"])
def confirm_app_is_running():
    return "Welcome to the Scissor app :)"


app.include_router(user_router, prefix="/user", tags=["User Routes"])
app.include_router(url_router, prefix="/url", tags=["URL Routes"])
