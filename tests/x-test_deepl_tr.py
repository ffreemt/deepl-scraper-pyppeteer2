"""Test deepl_tr."""
#

import asyncio
import atexit
import pyppeteer

import pytest
from logzero import logger

# from get_ppbrowser.get_ppbrowser import get_ppbrowser
from deepl_scraper_pp.deepl_tr import deepl_tr

# from deepl_scraper_pp.get_ppbrowser import get_ppbrowser


# @pytest.fixture(scope="session")
@pytest.fixture(scope="function")
async def prep_page_loop():
    """Prep page.

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop): any use?
     https://stackoverflow.com/questions/49936724/async-fixtures-with-pytest
     pytest quick guide epub book, scopte in action

    browser = asyncio.get_event_loop().run_until_complete(pyppeteer.launch())

    async def cleanup_async():
        await browser.quit()

    @atexit.register
    def cleanup():
        asyncio.get_event_loop().run_until_complete(cleanup_async())

    handling pyppeteer.launch
    https://github.com/d33tah/html2pdf/blob/master/server.py#L33
    """
    # browser = await get_ppbrowser(autoClose=False)

    loop = asyncio.get_event_loop()
    browser = await pyppeteer.launch()

    async def cleanup_async():
        await browser.close()
        loop.close()

    @atexit.register
    def cleanup():
        try:
            asyncio.get_event_loop().run_until_complete(cleanup_async())
        except Exception as exc:
            logger.error(exc)

    page = await browser.newPage()
    _ = "https://www.deepl.com/translator"
    await page.goto(_)
    # return page

    yield page, loop
    try:
        await page.close()
        # await browser.close()
    except Exception as exc:
        logger.error(exc)


_ = """
@pytest.fixture(scope='function')
async def fpage(prep_page):
    return prep_page
# """


@pytest.mark.asyncio
async def test_deepl_tr_aysnc(prep_page_loop):
    # async def test_deepl_tr():
    # def test_deepl_tr():
    """Test test_deepl_tr."""
    #

    # TODO: @pytest.fixture
    # browser = await get_ppbrowser(autoClose=False)
    # page = await browser.newPage()

    text = "test this and that"
    try:
        res = await deepl_tr("a", page=prep_page_loop[0])
        res = await deepl_tr(text, to_lang="zh", page=prep_page_loop[0])
        # res = LOOP.run_until_complete(deepl_tr("a"))
        # res = LOOP.run_until_complete(deepl_tr(text, to_lang="zh"))
        assert "试" in res
    except Exception as exc:
        logger.error(exc)
        # raise SystemExit(1) from exc  # should not be in a test
        assert False
    finally:
        await asyncio.sleep(100)
        # await page.close()
        # await browser.close()
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(loop.shutdown_asyncgens())
        # loop.close()

    # assert '试' in res


def test_deepl_tr_sync(prep_page_loop):
    _ = """
    try:
        loop = asyncio.get_event_loop()
    except Exception as exc:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    # """
    prep_page, loop = prep_page_loop
    asyncio.set_event_loop(loop)

    text = "test this and that"
    try:
        res = asyncio.run(deepl_tr("a", page=prep_page))
        res = asyncio.run(deepl_tr(text, to_lang="zh", page=prep_page))
        # res = LOOP.run_until_complete(deepl_tr("a"))
        # res = LOOP.run_until_complete(deepl_tr(text, to_lang="zh"))
        assert "试" in res
    except Exception as exc:
        logger.error(exc)
        assert False
