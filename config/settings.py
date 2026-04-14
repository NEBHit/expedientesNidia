from pydantic_settings import BaseSettings

#Clase de seteo de variables para el envio de mails
class Settings(BaseSettings):

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_TLS: bool
    MAIL_SSL: bool

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()