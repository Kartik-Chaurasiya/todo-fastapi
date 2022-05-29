from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from . import models, config
from .database import engine
from .routers import user, auth, todo

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(todo.router)
app.include_router(user.router)
app.include_router(auth.router)

#start server
# uvicorn api.app:app --reload  

