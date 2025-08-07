from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import redis.asyncio as redis
import os

# Seguridad
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

from .routes import router

load_dotenv()
TIMES = 1
SECONDS = 5
dependencies = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    redisCn = False
    host = os.getenv("REDIS_HOST", "host.docker.internal")
    port = int(os.getenv("REDIS_PORT", 6379))
    password = os.getenv("REDIS_PASSWORD")
    ssl_enabled = os.getenv("REDIS_SSL", "True").lower() == "true"

    # Conectarse a Redis usando los parámetros separados
    redis_connection = redis.Redis(
        host=host,
        port=port,
        password=password,
        ssl=ssl_enabled,
        decode_responses=True,
    )

    try:
        await redis_connection.ping()
        print("Conexión a Redis exitosa")

        await FastAPILimiter.init(redis_connection)
        print("FastAPILimiter inicializado.")

        redisCn = True
        dependencies = [Depends(RateLimiter(times=TIMES, seconds=SECONDS))]
    except Exception as e:
        print(f"Conexión a Redis fallida: {e}")

    yield

    if redisCn:
        await FastAPILimiter.close()
        print("FastAPILimiter cerrado.")


app = FastAPI(
    title="MOPI",
    description="API de MOPI, desarrollada para descargar tu música favorita.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)


# Proxy headers fix for HTTPS
@app.middleware("http")
async def https_scheme(request, call_next):
    x_forwarded_proto = request.headers.get("X-Forwarded-Proto")
    if x_forwarded_proto == "https":
        request.scope["scheme"] = "https"
    response = await call_next(request)
    return response


@app.get("/")
async def root() -> str:
    return app.description


app.include_router(router, dependencies=dependencies)
