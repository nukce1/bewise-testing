import logging
from contextlib import asynccontextmanager

from aiokafka import AIOKafkaProducer
from api.v1.applications import router as application_router
from config import settings
from database import sessionmanager
from fastapi import FastAPI


def init_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(application_router)

    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.basicConfig(
        level=settings.log_level,
        format=settings.log_format,
        datefmt=settings.log_date_format,
        filename=settings.log_path,
        filemode="a",
    )

    sessionmanager.init(settings.postgres_url)
    logging.info("База данных успешно подключена.")

    app.state.producer = AIOKafkaProducer(
        bootstrap_servers=settings.producer_servers, enable_idempotence=True, acks="all"
    )
    await app.state.producer.start()
    logging.info("Producer успешно запущен.")

    yield

    await app.state.producer.stop()
    logging.info("Producer успешно остановлен.")

    if sessionmanager.engine:
        await sessionmanager.close()
        logging.info("Подключение к базе данных успешно закрыто.")


app = init_app()
