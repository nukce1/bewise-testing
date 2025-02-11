# Инструкция по запуску проекта


 **Клонируйте репозиторий**

`git clone https://github.com/nukce1/bewise-testing.git`

 **Перейдите в репозиторий**

`cd bewise-testing/`
 
**Переименуйте файл конфигурации**

`mv BewiseTesting/.env_example BewiseTesting/.env`

**Запустите контейнеры**

`sudo docker compose up --build`

# Проверка работоспособности


 **Для отправки запросов используйте возможности FastAPI**

 `http://127.0.0.1:8000/docs#`

 
 **Для просмотра состояния брокера Kafka исползуйте UI**

  `http://localhost:8080/`

# Техническое задание
Сервис должен:

    - Принимать заявки через REST API (FastAPI).
    
    - Обрабатывать и записывать заявки в PostgreSQL.
    
    - Публиковать информацию о новых заявках в Kafka.
    
    - Обеспечивать эндпоинт для получения списка заявок с фильтрацией и пагинацией.
    
    - Включать Docker-файл для развертывания приложения.

# Примечание
Для упрощения стенда в проекте отсутствуют должные настройки шифрования данных, авторизации и сборки метрик для Kafka.
Аналогично не настроены параметры безопасного развертывания БД и приложения. 
