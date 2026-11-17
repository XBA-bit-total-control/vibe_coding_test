import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    DB_ENGINE = os.getenv("DB_ENGINE", "django.db.backends.postgresql")
    DB_NAME = os.getenv("DB_NAME", "postgres")
    DB_HOST = os.getenv("DB_HOST", "postgres")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

    SECRET_KEY = os.getenv("SECRET_KEY")
    if SECRET_KEY is None or SECRET_KEY == "" or not isinstance(SECRET_KEY, str):
        raise ValueError("SECRET_KEY не задан или некорректен")

    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1").split(",")
