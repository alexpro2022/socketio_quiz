from typing import Callable
import aiohttp
from .conftest import AppTest, pytestmark  # noqa

URL = AppTest.base_url


class Path:
    LARISKA = 'static/lariska.js'
    SCRIPT = 'static/script.js'
    STILE = 'static/style.css'


class LoadFailMsg:
    INDEX_HTML = "Не удалось загрузить страницу index.html"
    LARISKA = "Не удалось подгрузить lariska.js"
    SCRIPT = "Не удалось подгрузить script.js"
    STILE = "Не удалось подгрузить style.css"


async def get_response(
    session: aiohttp.ClientSession,
    path_param: str = '',
    error_msg: str = '',
    encoding: str = 'utf-8',
    check_response: Callable | None = None,
) -> str:
    async with session.get(f'/{path_param}') as response:
        assert response.status == 200, f'{response.status}: {error_msg}'
        if check_response is not None:
            return await check_response(response)
        return await response.text(encoding)


async def test__static():
    """
    Тест проверяет что сервер отдаёт index.html и все необходимые статические файлы подгружаются
    """
    async with aiohttp.ClientSession(URL) as session:
        page_content = await get_response(session, error_msg=LoadFailMsg.INDEX_HTML)
        script_text = '<script src="/{}"></script>'
        assert script_text.format(Path.LARISKA) in page_content
        assert script_text.format(Path.SCRIPT) in page_content
        assert f'<link rel="stylesheet" type="text/css" href="/{Path.STILE}"/>' in page_content

        # check that all static files are loaded
        assert await get_response(session, Path.LARISKA, LoadFailMsg.LARISKA)
        assert await get_response(session, Path.SCRIPT, LoadFailMsg.SCRIPT)
        assert await get_response(session, Path.STILE, LoadFailMsg.STILE)
