import uvicorn
from app.config import AppConfig

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=AppConfig.HOST,
        port=AppConfig.PORT,
        workers=AppConfig.WORKERS,
        log_level="info",
        reload=AppConfig.DEBUG,
        access_log=False
    )