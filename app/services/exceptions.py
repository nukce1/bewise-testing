

class WrongApplicationDataException(Exception):

    def __init__(self, message="Данные заявки не корректны."):
        self.message = message
        super().__init__(self.message)


class ProducerTimeoutException(Exception):
    def __init__(self, message="Таймаут ожидания ответа от брокера."):
        self.message = message
        super().__init__(self.message)
