"""Test deepl_tr."""
#

# import pytest
from logzero import logger

from get_ppbrowser import LOOP

from deepl_scraper_pp.deepl_tr import deepl_tr


# @pytest.mark.asyncio
# async def test_deepl_tr():
def test_deepl_tr():
    """Test test_deepl_tr."""

    text = "test this and that"
    try:
        # res = await deepl_tr(text)
        res = LOOP.run_until_complete(deepl_tr(text))
    except Exception as exc:
        logger.error(exc)
        raise SystemExit(1) from exc

    assert res
