import asyncio
from pathlib import Path
from urllib.parse import urlparse

import aiofiles
import aiohttp
from bs4 import BeautifulSoup

from config import settings
from utils import handle_images, make_url


async def parse_content(content: str) -> tuple[str, str]:
    soup = BeautifulSoup(content)
    posts = soup.find_all('div', class_='j_d_post_content')
    await handle_images(posts)

    title = soup.find('h3', class_='core_title_txt')
    if not title:
        title = soup.find('h1', class_='core_title_txt')
    if title:
        title = title.text.strip()

    return '\n***\n'.join(map(lambda x: x.prettify(), posts)), title or ''


async def run(url: str, path: Path):
    url = make_url(url, see_lz=1)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                print('请求异常:')
                print(resp.content)

            ret = await resp.text()
            content, title = await parse_content(ret)
            if not title:
                title = Path(urlparse(url).path).name

            async with aiofiles.open(path / Path(title + '.md'), 'w') as f:
                await f.write(f'# {title} \n{content}')


async def run_batch(*url: str):
    path = Path(settings.STORAGE) / Path('tieba')
    if not path.exists():
        path.mkdir(parents=True)

    tasks = []
    for u in url:
        tasks.append(run(u, path))
    await asyncio.gather(*tasks)


def tieba(url: list[str]):
    asyncio.run(run_batch(*url))


if __name__ == '__main__':
    asyncio.run(run('https://tieba.baidu.com/p/7446831583?page=1', Path('./')))
