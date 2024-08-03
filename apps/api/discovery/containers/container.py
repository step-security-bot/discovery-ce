from typing import Callable

import docker

from ..core.config import DockerConfig
from .volume import Volume


class Container:
    def __init__(
        self,
        docker_config: DockerConfig,
        docker_client: docker.DockerClient = None,
    ) -> None:
        self._docker_config = docker_config
        self._docker_client = docker_client or self._init_docker_client()

    def _init_docker_client(self) -> docker.DockerClient:
        try:
            docker_config = self._docker_config
            return docker.DockerClient(
                base_url=docker_config.docker_host,
                tls=docker.tls.TLSConfig(
                    client_cert=(
                        docker_config.docker_client_cert,
                        docker_config.docker_client_key,
                    ),
                    verify=False,
                ),
            )
        except docker.errors.DockerException as err:
            raise RuntimeError("Docker is not running, or not configured.") from err

    async def run(
        self,
        image: str,
        command: str,
        volume: Volume,
        on_create: Callable | None = None,
        on_start: Callable | None = None,
        on_finish: Callable | None = None,
    ) -> None:
        self._validate_image(image)

        if on_create:
            await on_create()

        container = self._create_container(image=image, command=command, volume=volume)

        if on_start:
            await on_start()

        container.wait()

        if on_finish:
            await on_finish()

    def _create_container(
        self,
        image: str,
        command: str,
        volume: Volume,
    ) -> any:
        docker_config = self._docker_config
        return self._docker_client.containers.run(
            detach=True,
            image=image,
            network_mode=docker_config.network_mode,
            security_opt=docker_config.security_options,
            cap_drop=["ALL"],
            mem_limit=docker_config.limits.memory,
            volumes={v.host: {"bind": v.guest, "mode": v.mode.value} for v in [volume]},
            command=command,
        )

    def _validate_image(self, image: str) -> None:
        if image not in self._docker_config.allowed_images:
            raise ValueError(f'Image "{image}" is not allowed')
