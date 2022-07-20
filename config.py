from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    QINIU_ACCESS_KEY: str
    QINIU_SECRET_KEY: str
    QINIU_BUCKET: str
    QINIU_HOST: AnyHttpUrl
    STORAGE: str = 'images'
    OUTDIR: str = 'output'
    LOCAL: bool = False

    class Config:
        env_file = '.env'

    @property
    def img_dir(self):
        return f'{self.OUTDIR}/tieba/images' if self.LOCAL else self.STORAGE


settings = Settings()
