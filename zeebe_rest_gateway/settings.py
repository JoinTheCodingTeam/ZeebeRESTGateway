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
    rest_job_timeout_ms = 10000
    rest_max_simultaneous_jobs = 4
    zeebe_worker_delay_after_error_ms = 100
    zeebe_worker_http_retry_delay_ms = 1000

    class Config:
        """Meta configuration"""
        env_file = ".env"
