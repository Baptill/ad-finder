from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# from api.router import user, ticket, collection, setting, media, cast, updating
from database.database import Base, engine

from database.schemas.user import User
from database.schemas.real_estate import (
    SellMedianPrice,
    RentMedianPrice,
    SellMedianPriceByRoom,
    RentMedianPriceByRoom,
    Appartment,
    House,
    TownRealEstate,
)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

print(f"🚀 Démarrage de l'application Ad Finder avec la base de données : {engine.url}")


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )


# app.include_router(user.router, prefix="/user")
# app.include_router(media.router, prefix="/media")
# app.include_router(cast.router, prefix="/cast")
# app.include_router(ticket.router, prefix="/ticket")
# app.include_router(collection.router, prefix="/collection")
# app.include_router(setting.router, prefix="/setting")
# app.include_router(updating.router, prefix="/updating")

# to access file
# app.mount("/storage", StaticFiles(directory="/app/back/storage"), name="storage")
