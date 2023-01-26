# deepl-scraper-pp2
[![tests](https://github.com/ffreemt/deepl-scraper-pyppeteer2/actions/workflows/routine-tests.yml/badge.svg)][![python](https://img.shields.io/static/v1?label=python+&message=3.8.3%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.8.3%2B&color=blue)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/deepl-scraper-pp.svg)](https://badge.fury.io/py/deepl-scraper-pp2)

scrape deepl using pyppeteer2 with para info, cross platform (Windows/MacOS/Linux)

## Intro
`deepl-scraper-pp2` is more or less deepl-scraper-pp. `deepl-scraper-pp2` however preserves newlines in the translated text. Hence, it will make life easier when trying to process large chunks of text. `deepl-scraper-pp2` is intended for `deepl-fastapi2` used in `deepl-tr-webui`.

## Installation

```bash
pip install deepl-scraper-pp2
# pip install deepl-scraper-pp2  # upgrade to the latest version
```
or
```bash
poetry add deepl-scraper-pp2
# poetry add deepl-scraper-pp2@latest  # upgrade to the latest version
```

or clone the repo (``git clone https://github.com/ffreemt/deepl-scraper-pyppeteer2.git``) and install from it.

## Usage

## In an `ipython` session:

```python

# ipython

from deepl_scraper_pp2.deepl_tr import deepl_tr

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
from deepl_scraper_pp2.deepl_tr import deepl_tr

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

# output: ['考我', 'Pyppeteer的API与puppeteer几乎相同。更多的API在文档中列出']

```

## Disclaimer

The pypi is beta and will likely remain beta -- use it at your own peril.

<!---

In [367]: doc0("div.lmt__textarea.lmt__textarea_dummydiv").text()
Out[367]: 'test you are me new lines 试探你是我 新行'

# doc0("div#target-dummydiv").text()
In [371]: doc0("#target-dummydiv").text()
Out[371]: '试探你是我 新行'

In [394]: doc0("#target-dummydiv").html()
Out[394]: '试探你是我\n新行\n\n'

# doc0("button.lmt__translations_as_text__text_btn").text()
In [369]: doc0(".lmt__translations_as_text__text_btn").text()
Out[369]: '试探你是我 新行'
In [369]: doc0(".lmt__translations_as_text__text_btn").html()


In [388]: re.findall(r"<button class=\"lmt__translations_as_text__text_btn[\s\S]*?>[\s\S]*?<\/button>", text0)
Out[388]: ['<button class="lmt__translations_as_text__text_btn">试探你是我\n新行</button>']

re.findall(r"<div id=\"target-dummydiv[\s\S]*?>[\s\S]*?<\/div>", text0)
['<div id="target-dummydiv" class="lmt__textarea lmt__textarea_dummydiv">试探你是我\n新行\n\n</div>']


extract format:  no need of html.escape

textarea = await page.wait_for_selector('//textarea', timeout=1 * 1000)

re.findall(r'lmt__translations_as_text__text_btn">([\s\S]+?)<\/button>', doc.html())
  re.findall(r'lmt__translations_as_text__text_btn">([\s\S]+?)<\/button>', await page.content())

===
from get_pwbrowser import get_pwbrowser

browser = await get_pwbrowser(headless=False)
context = await browser.new_context()
page = await context.new_page()

url = 'https://translate.google.cn/?sl=auto&tl=zh-CN&op=translate'
url = 'https://www.deepl.com/translator'
await page.goto(url)  # 10 s

textarea = await page.wait_for_selector('//textarea', timeout=1 * 1000)

sel_btn = "button.lmt__clear_text_button"

with CodeTimer():
    for text in [' test 1 ' * 10, ' test 2 ' * 10, ' test 3' *10]:
        # await textarea.fill('a')
        # await textarea.fill('a')

        # await page.evaluate(f'() => document.querySelectorAll("{sel_btn}")')

        _ = await is_visible(sel_btn, page)
        if _:
            clear_button = await page.wait_for_selector(f"{sel_btn}", timeout=1000)
            await clear_button.click()
        await textarea.fill(text)

        idx = 0
        flag = False
        ulimit = 1 / 0.1
        while not flag and idx < ulimit:
            idx += 1
            content = await page.content()
            doc = pq(content)

            flag = re.findall(r'lmt__translations_as_text__text_btn', doc.html())
            logger.debug(flag)
            if flag:
                break
            await asyncio.sleep(0.1)
        logger.info("loop: %s", idx)

        res = re.findall(r'lmt__translations_as_text__text_btn">([\s\S]+?)<\/button>', await page.content())
        print(res)
        # does not work for long text!

# https://stackoverflow.com/questions/47712679/how-can-i-check-that-an-element-is-visible-with-puppeteer-and-pure-javascript
selector = 'button.lmt__clear_text_button'

let elem = document.querySelector(selector);
const style = getComputedStyle(elem);
const rect1 = elem.getBoundingClientRect();
style.visibility !== 'hidden' && !!(rect1.bottom || rect1.top || rect1.height || rect1.width);

# ==
const element_is_visible = await page.evaluate(() => {
  const element = document.querySelector('button.lmt__clear_text_button');
  const style = getComputedStyle(element);
  const rect = element.getBoundingClientRect();

  return style.visibility !== 'hidden' && !!(rect.bottom || rect.top || rect.height || rect.width);
});

await textarea.fill(text)

str_ = f"""const element = document.querySelector('{sel_btn}');
  const style = getComputedStyle(element);
  const rect = element.getBoundingClientRect();
  return style.visibility !== 'hidden' && !!(rect.bottom || rect.top || rect.height || rect.width);"""
# visibility
visibility = await page.evaluate(f'() => {{{str_}}}')
print('visibility', visibility)

if visibility:
    cbtn= await page.wait_for_selector(f"{sel_btn}", timeout=1000)
    await cbtn.click(timeout=1000, no_wait_after=True)

async def is_visible(selector, page):
    _ = f"""const element = document.querySelector('{selector}'); if (element === null) return false;
  const style = getComputedStyle(element);
  const rect = element.getBoundingClientRect();
  return style.visibility !== 'hidden' && !!(rect.bottom || rect.top || rect.height || rect.width);"""
    return await page.evaluate(f'() => {{{_}}}')

async def console_run(js, page):
    _ = f'() => {js}'
    print(_)
    return await page.evaluate(_)

--->