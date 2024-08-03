from dataclasses import dataclass
from os import getenv

from pytz import timezone


@dataclass
class CeleryConfig:
    broker_url: str
    result_backend: str


@dataclass
class DockerConfig:
    allowed_images: list[str]
    security_options: list[str]
    capabilities: list[str]
    network_mode: str
    volumes_path: str
    limits: "DockerLimits"
    docker_host: str
    docker_client_cert: str
    docker_client_key: str


@dataclass
class DockerLimits:
    cpu: int
    memory: str
    read_only: bool


@dataclass
class PusherConfig:
    app_id: str
    key: str
    secret: str
    cluster: str


@dataclass
class S3Config:
    endpoint_url: str
    access_key_id: str
    secret_access_key: str
    region_name: str
    bucket_name: str
    verify_ssl: bool


class Config:
    def __init__(self) -> None:
        self._celery_config = self._get_celery_config()
        self._docker_config = self._get_docker_config()
        self._database_url = getenv("DATABASE_URL", "")
        self._base_url = getenv("BASE_URL", "http://127.0.0.1:8000")
        self._timezone = getenv("TIMEZONE", "UTC")
        self._pusher_config = self._get_pusher_config()
        self._s3_config = self._get_s3_config()

    def _get_celery_config(self) -> CeleryConfig:
        return CeleryConfig(
            broker_url=getenv("BROKER_URL", "redis://redis:6379/0"),
            result_backend=getenv("BACKEND_URL", "redis://redis:6379/0"),
        )

    def _get_docker_config(self) -> DockerConfig:
        return DockerConfig(
            allowed_images=self._parse_env_list("DOCKER_ALLOWED_IMAGES"),
            security_options=self._parse_env_list("DOCKER_SECURITY_OPTIONS"),
            capabilities=self._parse_env_list("DOCKER_CAPABILITIES"),
            network_mode=getenv("DOCKER_NETWORK_MODE", "bridge"),
            volumes_path=getenv("DOCKER_VOLUMES_PATH", "/tmp"),
            limits=self._get_docker_limits(),
            docker_host=getenv("DOCKER_HOST", None),
            docker_client_cert=getenv("DOCKER_CLIENT_CERT", None),
            docker_client_key=getenv("DOCKER_CLIENT_KEY", None),
        )

    def _get_docker_limits(self) -> DockerLimits:
        return DockerLimits(
            cpu=int(getenv("DOCKER_LIMITS_CPU", 1)),
            memory=getenv("DOCKER_LIMITS_MEMORY", "50M"),
            read_only=bool(getenv("DOCKER_LIMITS_READ_ONLY", True)),
        )

    def _get_pusher_config(self) -> PusherConfig:
        return PusherConfig(
            app_id=getenv("PUSHER_APP_ID"),
            key=getenv("PUSHER_KEY"),
            secret=getenv("PUSHER_SECRET"),
            cluster=getenv("PUSHER_CLUSTER"),
        )

    def _get_s3_config(self) -> S3Config:
        return S3Config(
            endpoint_url=getenv("AWS_S3_ENDPOINT", None),
            access_key_id=getenv("AWS_S3_ACCESS_KEY_ID", None),
            secret_access_key=getenv("AWS_S3_SECRET_ACCESS_KEY", None),
            region_name=getenv("AWS_S3_REGION", None),
            bucket_name=getenv("AWS_S3_BUCKET_NAME"),
            verify_ssl=(getenv("AWS_S3_VERIFY_SSL", "False") == "True"),
        )

    @property
    def celery_config(self) -> CeleryConfig:
        return self._celery_config

    @property
    def docker_config(self) -> DockerConfig:
        return self._docker_config

    @property
    def database_url(self) -> str:
        return self._database_url

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def timezone(self) -> timezone:
        return timezone(self._timezone)

    @property
    def pusher_config(self) -> PusherConfig:
        return self._pusher_config

    @property
    def s3_config(self) -> S3Config:
        return self._s3_config

    def _parse_env_list(self, key: str) -> list[str]:
        value = getenv(key, None)
        return value.strip().split(",") if value else []
