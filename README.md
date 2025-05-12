1. заруск проекта
    1.1. запустите Docker вручную 
    1.2 зайдиту в папку с docker-compose.yml 
    1.3 запустите docker-compose.yml: docker-compose up --build (на сервере желательно с sudo)


пример .env фала:
    DB_USER=postgres
    DB_PASS=your_db_password
    DB_NAME=your_db_name
    DB_HOST=db                      # в docker это будет контейнер db
    DB_PORT=5432
    SECRET_KEY=your_secret_key
    SECRET_KEY_VERIFY=your_secret_key_for_verify
    ALGORITHM=HS256
    REDIS_HOST=redis               # в docker это будет контейнер redis
    REDIS_PORT=6379
    MAIL_USERNAME=example@gmail.com
    MAIL_PASSWORD=xxxx xxxx xxxx xxxx
    MAIL_FROM=example@gmail.com
    MAIL_PORT=587
    MAIL_SERVER=smtp.gmail.com
    MAIL_STARTTLS=True
    MAIL_SSL_TLS=False
    USE_CREDENTIALS=True
    DNS_URL=http://localhost:8081 # это для отправки правильного url при верификации
    JWT_ACCESS_EXPIRE_MINUTES=30
    JWT_REFRESH_EXPIRE_DAYS=7

