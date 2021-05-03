from urllib.parse import urljoin

global HOST
global PORT
global API_PROTO
global LOG_LEVEL
global BASE_PATH
global TREASURE_PATH
global USER_DATA_PATH
global WINNER_MAIL_ADDRESS


def riddle_url(route: str) -> str:
    return urljoin(f'{API_PROTO}://{HOST}:{PORT}/', f'{route}')
