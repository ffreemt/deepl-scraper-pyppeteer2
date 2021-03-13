"""Scrape deepl via pyppeteer.

org deepl4a

set PYTHONPATH=../get-ppbrowser

from pathlib import Path
import os
os.environ['PYTHONPATH'] = Path(r"../get-ppbrowser")
"""
#

from typing import Union

import asyncio
from urllib.parse import quote
from pyquery import PyQuery as pq
import logzero
from logzero import logger
from linetimer import CodeTimer

with CodeTimer(name="loading BROWER", unit="s"):
    # from deepl_tr_pp.deepl_tr_pp import deepl_tr_pp, LOOP, BROWSER, get_ppbrowser
    from get_ppbrowser.get_ppbrowser import LOOP, BROWSER, get_ppbrowser

with CodeTimer(name="start a page", unit="s"):
    URL = r"https://www.deepl.com/translator"
    # URL = 'https://www.deepl.com/translator#auto/zh/'
    PAGE = LOOP.run_until_complete(BROWSER.newPage())
    try:
        LOOP.run_until_complete(PAGE.goto(URL, timeout=45 * 1000))
    except Exception as exc:
        logger.error("exc: %s, exiting", exc)
        raise SystemExit(
            "Unable to make initial connection to deelp"
        ) from exc


# fmt: off
async def deepl(
        text: str,
        from_lang: str = "auto",
        to_lang: str = "zh",
        page=PAGE,
        verbose: Union[bool, int] = False,
        timeout: float = 5,
):
    # fmt: on
    """Deepl via pyppeteer.

    text = "Test it and more"
    from_lang="auto"
    to_lang="zh"
    page=PAGE
    verbose=True
    """
    #

    if isinstance(verbose, bool):
        if not verbose:
            logzero.setup_default_logger(level=20)
    else:
        logzero.setup_default_logger(level=verbose)

    logger.debug(" Entry ")

    url0 = f"{URL}#{from_lang}/{to_lang}/"

    url_ = f"{URL}#{from_lang}/{to_lang}/{quote(text)}"

    selector = ".lmt__language_select--target > button > span"

    with CodeTimer(name="fetching", unit="s"):
        _ = """
        await page.goto(url0)

        try:
            await page.waitForSelector(selector, timeout=8000)
        except Exception as exc:
            raise
        # """

        doc = pq(await page.content())
        text_old = doc('#source-dummydiv').text()
        logger.debug("Old source: %s", text_old)

        try:
            deepl.first_run
        except AttributeError:
            deepl.first_run = 1
            text_old = "_some unlikely random text_"

        selector = "div.lmt__translations_as_text"
        if text.strip() == text_old.strip():
            logger.debug("%s, early result:  %s", text, doc('.lmt__translations_as_text__text_btn').text())
            doc = pq(await page.content())
            content = doc('.lmt__translations_as_text__text_btn').text()
        else:
            # record content
            try:
                # page.goto(url_)
                await page.goto(url0)
            except Exception as exc:
                logger.error(exc)
                raise

            try:
                await page.waitForSelector(".lmt__translations_as_text", timeout=20000)
            except Exception as exc:
                logger.error(exc)
                raise

            doc = pq(await page.content())
            content_old = doc('.lmt__translations_as_text__text_btn').text()

            selector = ".lmt__translations_as_text"
            selector = ".lmt__textarea.lmt__target_textarea.lmt__textarea_base_style"

            selector = ".lmt__textarea.lmt__target_textarea"
            selector = '.lmt__translations_as_text__text_btn'
            try:
                await page.goto(url_)
            except Exception as exc:
                logger.error(exc)
                raise

            try:
                await page.waitForSelector(".lmt__translations_as_text", timeout=20000)
            except Exception as exc:
                logger.error(exc)
                raise

            doc = pq(await page.content())
            content = doc('.lmt__translations_as_text__text_btn').text()

            logger.debug(
                "content_old: [%s], \n\t content: [%s]",
                content_old, content
            )

            # loop until content changed
            idx = 0
            # bound = 50  # 5s
            while idx < timeout:
                idx += 1
                await asyncio.sleep(.1)
                doc = pq(await page.content())
                content = doc('.lmt__translations_as_text__text_btn').text()
                logger.debug("content_old: %s, content: %s", content_old, content)

                if content_old != content and bool(content):
                    break

            logger.debug(" loop: %s", idx)

    logger.debug(" Fini ")

    return content


if __name__ == "__main__":
    import sys

    text = "test this and that and more"
    res = LOOP.run_until_complete(deepl(text))
    logger.info("%s, %s,", text, res)

    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = "test this and that"

    res = LOOP.run_until_complete(deepl(text))
    logger.info("%s, %s,", text, res)

    # text = "what's the matter?"
    # res = LOOP.run_until_complete(deepl(text))
    # logger.info("%s, %s,", text, res)