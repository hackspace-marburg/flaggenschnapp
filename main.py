import uvicorn

from api import API
import config


def main():
    uvicorn.run(
        app=API(),
        host=config.HOST,
        port=config.PORT,
        log_level=config.LOG_LEVEL
    )


if __name__ == '__main__':
    main()
