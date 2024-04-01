from fastapi import FastAPI
from routes.route import router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(docs_url="/docs", openapi_url="/openapi.json")
app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def hello():
    return "HELLO!"
