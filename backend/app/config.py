from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_username: str
    database_port: str
    database_password: str
    database_name: str
    
    jwt_secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    jwt_refresh_secret_key: str

    class Config:
        env_file = ".env"
page_size = 10

settings = Settings()