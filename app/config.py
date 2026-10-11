from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://quests:quests@localhost:5432/quests"
    data_dir: str = "./data"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
