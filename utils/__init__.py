import asyncio
import datetime
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlunparse
from urllib.parse import urlparse

import aiofiles
import aiohttp
from bs4 import Tag

from config import settings
# from utils.qiniu_oss import make_full_url, upload
from utils.github import make_full_url, upload


def make_url(url: str, **query):
    parsed = urlparse(url)
    query_params: dict[str, str] = dict(parse_qsl(parsed.query))
    query_params.update(query)
    url = urlunparse((
        parsed.scheme,
        parsed.hostname,
        parsed.path,
        parsed.params,
        urlencode(query_params),
        parsed.fragment))
    return url


async def save_img(url: str, name: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                print('error: %s', resp.content)

            localpath = Path(settings.img_dir) / Path(name)
            if not localpath.parent.exists():
                localpath.parent.mkdir(parents=True)
            async with aiofiles.open(localpath, 'wb') as f:
                content = await resp.content.read()
                await f.write(content)

    upload(name, str(localpath))


async def handle_images(tags: list[Tag], **filters):
    tasks = []
    for t in tags:
        for img in t.find_all('img', **filters):
            name = Path(urlparse(img['src']).path).name
            name = f'{datetime.date.today().isoformat()}/{name}'
            tasks.append(save_img(img['src'], name))
            img['src'] = make_full_url(name)

    await asyncio.gather(*tasks)
