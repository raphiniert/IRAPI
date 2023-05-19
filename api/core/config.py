from pydantic import BaseSettings, Field, SecretStr


class Settings(BaseSettings):
    # router
    router_prefix: str = "/api"
    router_version_prefix: str = "/v1"

    # database
    db_server: str = Field(..., env="POSTGRES_SERVER")
    db_user: str = Field(..., env="POSTGRES_USER")
    db_password: SecretStr = Field(..., env="POSTGRES_PASSWORD")
    db_db: str = Field(..., env="POSTGRES_DB")
    db_port: str = Field(..., env="POSTGRES_PORT")

    # authentication
    private_key_pem: SecretStr = Field(..., env="PASETO_PRIVATE_KEY")
    public_key_pem: SecretStr = Field(..., env="PASETO_PUBLIC_KEY")
    access_token_expire_seconds: int = Field(..., env="ACCESS_TOKEN_EXPIRE_SECONDS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
