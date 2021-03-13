# deepl-scraper-pp
[![tests](https://github.com/ffreemt/deepl-scraper-pyppeteer/actions/workflows/routine-tests.yml/badge.svg)][![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/deepl-scraper-pp.svg)](https://badge.fury.io/py/deepl-scraper-pp)

scrape deepl using pyppeteer

## Installation

```bash
pip install deepl-scraper-pp
# pip install deepl-scraper-pp  # upgrade to the latest version
```
or
```bash
poetry add deepl-scraper-pp
# poetry add deepl-scraper-pp@latest  # upgrade to the latest version
```

or clone the repo (``git clone https://github.com/ffreemt/deepl-scraper-pyppeteer.git``) and install from it.

## Usage

## In an `ipython` session:

```python

# ipython

from deepl_scraper_pp.deepl_tr import deepl_tr

res = await deepl_tr("test me")
print(res)
# '考我 试探我 测试我 试探'

print(await deepl_tr("test me", to_lang="de"))
# mich testen mich prüfen testen Sie mich

text = "Pyppeteer has almost same API as puppeteer. More APIs are listed in the document"
print(await deepl_tr(text, to_lang="zh"))
# Pyppeteer的API与puppeteer几乎相同。更多的API在文档中列出。
```

## in `python`

```python
import asyncio
from deepl_scraper_pp.deepl_tr import deepl_tr

async def main():
    text1 = "test me"
    text2 = "Pyppeteer has almost same API as puppeteer. More APIs are listed in the document"

    coros = [deepl_tr(elm) for elm in [text1, text2]]
    res = await asyncio.gather(*coros, return_exceptions=True)
    print(res)

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
finally:
    loop.close()

# output: ['考我 试探我 测试我 试探', 'Pyppeteer的API与puppeteer几乎相同。更多的API在文档中列出']

```

## Disclaimer

The pypi is beta and will likely remain beta -- use it at your own peril.