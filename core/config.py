
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Annotated, Literal, Any

from pydantic import (
    AnyUrl,
    BeforeValidator,
    computed_field,
    PostgresDsn, 
    Field
)

from pydantic_core import MultiHostUrl


# Function to parse CORS origins, handling string and list types
def parse_cors(v: Any) -> list[list[str], str]:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, (list, str)):
        return v
    raise ValueError(v)

class Settings(BaseSettings):
    # Configuration for the environment file
    model_config = SettingsConfigDict(env_file='.env', env_ignore_empty=True, extra="ignore")
    
    # Basic settings
    DOMAIN: str = 'localhost'
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    POSTGRESQL_USER: str
    POSTGRESQL_PASSWORD: str
    POSTGRESQL_SERVER: str
    POSTGRESQL_PORT: int
    POSTGRESQL_DB: str

    # SQLite settings
    SQLITE_DB_PATH: str = 'db1.db'  # Default SQLite DB path

    # CORS settings (for your front-end apps)
    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []


    @computed_field
    @property
    def server_host(self) -> str:
        # Use HTTPS for anything other than local development
        if self.ENVIRONMENT == "local":
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}"

    @computed_field  # Type: ignore[misc]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        """
        Based on the environment, return the correct database URI.
        Supports both SQLite and PostgreSQL.
        """
        if self.ENVIRONMENT == "local":
            # Use SQLite when in local environment
            return f"sqlite+aiosqlite:///{self.SQLITE_DB_PATH}"
        elif self.ENVIRONMENT in ["staging", "production"]:
            # Use PostgreSQL in production or staging environments
            return f"postgresql+asyncpg://{self.POSTGRESQL_USER}:{self.POSTGRESQL_PASSWORD}" \
                   f"@{self.POSTGRESQL_SERVER}:{self.POSTGRESQL_PORT}/{self.POSTGRESQL_DB}"
        else:
            raise ValueError("Unsupported environment for database connection")

    

# Initialize settings
settings = Settings()
