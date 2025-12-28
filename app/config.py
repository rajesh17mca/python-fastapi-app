import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    CURRENCY_EXCHANGE_API_KEY = os.getenv("CURRENCY_EXCHANGE_API_KEY")
    LOG_FILE = "logs/app.log"

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    LOG_FILE = "logs/dev_app.log"

class AppConfig:
    HOST = "0.0.0.0"
    PORT = 8080
    WORKERS = 1
    DEBUG = True
    LOG_FILE = "logs/app.log"