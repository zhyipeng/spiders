from qiniu import Auth, etag, put_file

from config import settings

q = Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)


def upload(filepath: str, localpath: str):
    token = q.upload_token(settings.QINIU_BUCKET, filepath)
    ret, info = put_file(token, filepath, localpath)
    assert ret['key'] == filepath
    assert ret['hash'] == etag(localpath)


def make_full_url(path: str) -> str:
    return f'{settings.QINIU_HOST}/{path}'
