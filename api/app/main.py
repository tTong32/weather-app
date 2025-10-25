from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# routers
from app.routes.current import router as current_router
from app.routes.forecast import router as forecast_router
# db init
from app.repository.db import init_db

app = FastAPI(title="Weather App API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://localhost:?.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

app.include_router(current_router, prefix="/api/weather")
app.include_router(forecast_router, prefix="/api/weather")


@app.get("/")
def root():
    return {"status": "ok", "message": "Weather API - try /api/weather/current?location=Toronto"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)