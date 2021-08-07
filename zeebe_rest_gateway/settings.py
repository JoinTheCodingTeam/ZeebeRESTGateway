"""
Service settings.
"""
from pydantic import BaseSettings, PositiveInt


class Settings(BaseSettings):
    """Service settings."""
    zeebe_hostname: str
    zeebe_port: int = 26500
    zeebe_publish_retry_attempts: PositiveInt = 5
    zeebe_publish_retry_delay_ms: PositiveInt = 300

    class Config:
        """Meta configuration"""
        env_file = ".env"
