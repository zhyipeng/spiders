from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    QINIU_ACCESS_KEY: str
    QINIU_SECRET_KEY: str
    QINIU_BUCKET: str
    QINIU_HOST: AnyHttpUrl
    STORAGE: str = 'images'
    OUTDIR: str = 'output'

    class Config:
        env_file = '.env'


settings = Settings()
