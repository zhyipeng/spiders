from config import settings


def upload(filepath: str, localpath: str):
    pass


def make_full_url(path: str) -> str:
    if settings.LOCAL:
        return f'images/{path}'
    return f'https://raw.githubusercontent.com/zhyipeng/spiders/main/images/{path}'
