import uvicorn
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import (
    PlainTextResponse, RedirectResponse,
    FileResponse,
    )

fibo_count = 42


def fib(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


fibo_row = list(fib(fibo_count))

fibo_path = '/' + '/'.join(map(str, fibo_row))
maze_link = '/maze'
treasure_link = f'{fibo_path}/treasure'
print(f'treasure path is: {treasure_link}')
# treasure_link = f'/treasure'

app = Starlette(debug=True)
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.route('/maze/hint')
async def hint(request):
    message = '\tHere is your hint:\n\n' \
              '\ta+b is to a as a is to b.\n\n' \
              '\tThe answer to all questions is, quote:\n' \
              '\t\t\"[...] the sort of number that you could ' \
              'without any fear introduce to your parents\"' \
              '\n'

    return PlainTextResponse(message)


@app.route('/maze')
async def entrance(request):
    message = '\tWelcome to the maze.\n' \
              '\tYou will not succeed through brute force.\n' \
              '\tYou will not succeed by trying.\n' \
              '\tYou will succeed by following the path of which ' \
              'pleases the eye until ' \
              'the point that is the answer to all questions.\n\n' \
              '\tThose who disobey the rules will be left with some time ' \
              'to reflect upon themselves.\n\n' \
              '\tIf you need a hint, visit /maze/hint\n\n'

    return PlainTextResponse(message)


@app.route(treasure_link)
async def treasure(request):
    uvicorn.config.logger.info(f'client found the treasure: {request.client}')
    file_path = './data/data.dat'
    return FileResponse(path=file_path)


@app.route('/')
async def welcome(request):
    message = 'There is a MAZE hidden around here somewhere.\n' \
              'Go and find it.\n'
    return PlainTextResponse(message)


@app.route('/{full_path:path}')
@limiter.limit('60/minute')
async def miss(request: Request):
    full_path = request.path_params['full_path']
    uvicorn.config.logger.debug(f'client miss: /{full_path}')
    return RedirectResponse(url='/')


uvicorn.run(app, host="0.0.0.0", port=5000, log_level='debug')
