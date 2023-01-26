"""Scrape deepl via pyppeteer.

org deepl4a

set PYTHONPATH=../get-ppbrowser

from pathlib import Path
import os
os.environ['PYTHONPATH'] = Path(r"../get-ppbrowser")
"""
# pylint: disable=too-many-arguments, too-many-locals, too-many-branches, too-many-statements, broad-except
import asyncio

# import os
import re
import sys
from random import randint
from typing import Any, Callable, Optional, Union
from urllib.parse import quote

import logzero

# import pyppeteer
from about_time import about_time
from get_ppbrowser.get_ppbrowser import get_ppbrowser
from logzero import logger
from pyquery import PyQuery as pq

URL = r"https://www.deepl.com/translator"

_ = """
with CodeTimer(name="loading BROWER", unit="s"):
    # from deepl_tr_pp.deepl_tr_pp import deepl_tr_pp, LOOP, BROWSER, get_ppbrowser
    from get_ppbrowser.get_ppbrowser import LOOP, BROWSER

with CodeTimer(name="start a page", unit="s"):
    # URL = 'https://www.deepl.com/translator#auto/zh/'
    PAGE = LOOP.run_until_complete(BROWSER.newPage())
    try:
        LOOP.run_until_complete(PAGE.goto(URL, timeout=45 * 1000))
    except Exception as exc:
        logger.error("exc: %s, exiting", exc)
        raise SystemExit("Unable to make initial connection to deelp") from exc
# """


def with_func_attrs(**attrs: Any) -> Callable:
    """with_func_attrs"""

    def with_attrs(fct: Callable) -> Callable:
        for key, val in attrs.items():
            setattr(fct, key, val)
        return fct

    return with_attrs


@with_func_attrs(from_lang="", to_lang="", text="")
async def deepl_tr(
    text: str,
    from_lang: str = "auto",
    to_lang: str = "zh",
    page=None,
    verbose: Union[bool, int] = False,
    timeout: float = 5,
    headless: Optional[bool] = None,
):
    """Deepl via pyppeteer.

    text = "Test it and\n\n more"
    from_lang="auto"
    page=None
    to_lang="zh"
    verbose=True
    """
    #

    # set verbose=40 to turn most things off
    if isinstance(verbose, bool):
        if verbose:
            logzero.setup_default_logger(level=10)
        else:
            logzero.setup_default_logger(level=20)
    else:  # integer: log_level
        logzero.setup_default_logger(level=verbose)

    logger.debug(" Entry ")

    try:
        text = text.strip()
    except Exception as exc:
        logger.error(exc)
        logger.info(" not a string?")
        raise

    # if text remains the same but from_lang or to_lang changed, attach random string \d_
    # if text.strip() == deepl_tr.strip() and (deepl_tr.from_lang
    logger.debug(
        "text==deepl_tr.text: %s==%s, from_lang==deepl_tr.from_lang: "
        "%s==%s, to_lang==deepl_tr.to_lang: %s==%s",
        text,
        deepl_tr.text,
        from_lang,
        deepl_tr.from_lang,
        to_lang,
        deepl_tr.to_lang,
    )

    same_langs = from_lang == deepl_tr.from_lang and to_lang == deepl_tr.to_lang

    if text == deepl_tr.text:
        if not same_langs:
            deepl_tr.text = text
            _ = randint(1, 1000)
            logger.debug("attaching extra")
            text = f"{text} {_}_"
    logger.debug("text: %s", text)

    deepl_tr.from_lang = from_lang
    deepl_tr.to_lang = to_lang

    # reuse page
    try:
        _ = deepl_tr.page  # run previously
        page = deepl_tr.page
    except AttributeError:
        if page is None:
            try:
                if headless is None:
                    browser = get_ppbrowser()
                else:
                    browser = get_ppbrowser(headless=headless)
            except Exception as exc:
                logger.error(exc)
                raise

            try:
                page = await browser.newPage()
            except Exception as exc:
                logger.error(exc)
                raise

            url = r"https://www.deepl.com/translator"
            try:
                await page.goto(url, timeout=45 * 1000)
            except Exception as exc:
                logger.error(exc)
                raise

            deepl_tr.page = page
        else:
            deepl_tr.page = page

    page = deepl_tr.page

    url0 = f"{URL}#{from_lang}/{to_lang}/"

    url_ = f"{URL}#{from_lang}/{to_lang}/{quote(text)}"

    # selector = ".lmt__language_select--target > button > span"

    if verbose < 11 or verbose is True:
        _ = False  # silent
    else:
        _ = True
    # with CodeTimer(name="fetching", unit="s", silent=_):
    with about_time() as dur:
        _ = """
        await page.goto(url0)

        try:
            await page.waitForSelector(selector, timeout=8000)
        except Exception as exc:
            raise
        # """

        try:
            content = await page.content()
        except Exception as exc:
            logger.error(exc)
            raise

        doc = pq(content)
        text_old = doc("#source-dummydiv").html()
        logger.debug("Old source: %s", text_old)

        try:
            deepl_tr.first_run
        except AttributeError:
            deepl_tr.first_run = 1
            text_old = "_some unlikely random text_"

        logger.debug(
            "text.strip(): %s, text_old.strip(): %s", text.strip(), text_old.strip()
        )

        # selector = "div.lmt__translations_as_text"
        if text.strip() == text_old.strip() and same_langs:
            logger.debug(" ** early result: ** ")
            logger.debug(
                "%s, %s", text, doc(".lmt__translations_as_text__text_btn").text()
            )
            doc = pq(await page.content())
            # content = doc('.lmt__translations_as_text__text_btn').text()
            content = doc(".lmt__translations_as_text__text_btn").html()
        else:
            # record content
            try:
                # page.goto(url_)
                await page.goto(url0)
            except Exception as exc:
                logger.error(exc)
                raise

            try:
                # await page.waitForSelector(".lmt__translations_as_text", timeout=20000)
                await page.waitForSelector(".lmt__target_textarea", timeout=20000)
            except Exception as exc:
                logger.error(exc)
                raise

            doc = pq(await page.content())
            # content_old = doc('.lmt__translations_as_text__text_btn').text()
            content_old = doc(".lmt__translations_as_text__text_btn").html()

            # selector = ".lmt__translations_as_text"
            # selector = ".lmt__textarea.lmt__target_textarea.lmt__textarea_base_style"

            # selector = ".lmt__textarea.lmt__target_textarea"
            # selector = '.lmt__translations_as_text__text_btn'
            try:
                await page.goto(url_)
            except Exception as exc:
                logger.error(exc)
                raise

            try:
                # await page.waitForSelector(".lmt__translations_as_text", timeout=20000)
                await page.waitForSelector(".lmt__target_textarea", timeout=20000)
            except Exception as exc:
                logger.error(exc)
                raise

            doc = pq(await page.content())
            content = doc(".lmt__translations_as_text__text_btn").text()

            logger.debug("content_old: [%s], \n\t content: [%s]", content_old, content)

            # loop until content changed
            idx = 0
            # bound = 50  # 5s
            while idx < timeout / 0.1:
                idx += 1
                await asyncio.sleep(0.1)
                doc = pq(await page.content())
                content = doc(".lmt__translations_as_text__text_btn").html()
                logger.debug(
                    "content_old: (%s), \n\tcontent: (%s)", content_old, content
                )

                if content_old != content and bool(content):
                    break

            logger.debug(" loop: %s", idx)

    # deepl_tr.dur = dur
    deepl_tr.dur = dur.duration_human

    logger.debug(" Fini ")

    # await page.close()
    # await browser.close()
    # browser.process.communicate()

    # remove possible attached suffix
    content = re.sub(r"[\d]+_$", "", content.strip()).strip()

    return content


async def main():
    """Main."""
    text = "test this and that and more"
    res = deepl_tr(text)
    logger.info("%s, %s, time elased: %s", text, res, deepl_tr.dur)

    res = await deepl_tr(text, to_lang="de")

    logger.info("%s, %s, time elased: %s", text, res, deepl_tr.dur)

    # input("Press Enter to continue...")

    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = "test this and that"

    res = await deepl_tr(text)
    logger.info("%s, %s,", text, res)


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
    except Exception as exc_:
        logger.error(exc_)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(main())
    except Exception as exc_:
        logger.error(exc_)
    finally:
        loop.close()

    _ = """
    import sys

    text = "test this and that and more"
    res = LOOP.run_until_complete(deepl_tr(text))
    logger.info("%s, %s,", text, res)

    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = "test this and that"

    res = LOOP.run_until_complete(deepl_tr(text))
    logger.info("%s, %s,", text, res)

    # """
