"""Test simple."""
import asyncio
import pyppeteer
from deepl_scraper_pp2.deepl_tr import deepl_tr

# from get_ppbrowser.get_ppbrowser import get_ppbrowser


def test_simple():
    """Test simple.

    @pytest.fixture(scope="function")
    async def
        ...
    @pytest.mark.asyncio
        ...

    wont work, always runtime errors: loop already closed
    """
    try:
        loop = asyncio.get_event_loop()
    except Exception:
        # logger.error(exc)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # browser = asyncio.run(pyppeteer.launch())
    # page = asyncio.run(browser.newPage())

    # 3s
    browser = loop.run_until_complete(pyppeteer.launch())

    # also OK, 1.8s
    # browser = loop.run_until_complete(get_ppbrowser())

    # 500 ms
    page = loop.run_until_complete(browser.newPage())

    text = "test this and more"
    # res = asyncio.run(deepl_tr(text, page=page))

    # fist time ~10s, 3.25s
    res = loop.run_until_complete(deepl_tr(text, page=page))

    assert "试" in res


def test_para_info():
    """Test para_info."""
    try:
        loop = asyncio.get_event_loop()
    except Exception:
        # logger.error(exc)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # browser = asyncio.run(pyppeteer.launch())
    # page = asyncio.run(browser.newPage())

    # 3s
    browser = loop.run_until_complete(pyppeteer.launch())

    # also OK, 1.8s
    # browser = loop.run_until_complete(get_ppbrowser())

    # 500 ms
    page = loop.run_until_complete(browser.newPage())

    text = "test this \n\nand more"

    # res = await deepl_tr(text)
    res = loop.run_until_complete(deepl_tr(text, page))

    assert res.split("\n\n").__len__() == 2

    # loop.run_until_complete(page.close())
    # loop.run_until_complete(browser.close())


def test_para_info1():
    """Test para_info, no page provided."""
    try:
        loop = asyncio.get_event_loop()
    except Exception:
        # logger.error(exc)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    text = "test this \n\nand more"

    # res = await deepl_tr(text)
    res = loop.run_until_complete(deepl_tr(text))

    assert res.split("\n\n").__len__() == 2

    # use page from the previous call of deepl_tr
    loop.run_until_complete(deepl_tr.page.close())
    # loop.run_until_complete(deepl_tr.browser.close())
