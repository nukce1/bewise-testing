import logging

from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaTimeoutError
from app.config import settings
from app.domain.schemas import ApplicationDTO
from app.services.exceptions import ProducerTimeoutException


class KafkaProducerService:
    def __init__(self, producer: AIOKafkaProducer):
        self.producer = producer
        self.topic_applications_created = settings.topic_applications_created

    async def send_application_created(self, created_app: ApplicationDTO) -> None:
        """
        Отправляет брокеру данные созданной заявки.
        Args:
            created_app: Созданная заявка

        Returns:
            None
        """
        try:
            app_id: int = created_app.id
            app_data: str = created_app.model_dump_json()

            await self.producer.send_and_wait(
                topic=self.topic_applications_created,
                key=str(app_id).encode("utf-8"),
                value=app_data.encode("utf-8"),
            )
        except KafkaTimeoutError:
            logging.error(
                f"Ошибка при отправке данных заявки {app_id} в топик {self.topic_applications_created} "
            )
            raise ProducerTimeoutException()
