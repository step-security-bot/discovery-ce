from unittest.mock import AsyncMock, MagicMock

import docker
import pytest

from discovery.containers.container import Container
from discovery.containers.volume import Mode, Volume
from discovery.core.config import DockerConfig, DockerLimits


@pytest.fixture
def docker_config():
    limits = DockerLimits(cpu=1000, memory="1G", read_only=True)
    return DockerConfig(
        docker_host="https//pytest-docker",
        docker_client_cert="cert.pem",
        docker_client_key="cert.key",
        network_mode="bridge",
        security_options=["seccomp=unconfined"],
        limits=limits,
        allowed_images=["alpine", "busybox"],
        volumes_path="/host/volumes",
        capabilities=["CAP_NET_ADMIN", "CAP_SYS_ADMIN"],
    )


@pytest.fixture
def volume():
    return Volume(host="/host/path", guest="/guest/path", mode=Mode.READ_WRITE)


@pytest.fixture
def docker_client():
    return MagicMock(spec=docker.DockerClient)


def test_init_with_docker_client(docker_config, docker_client):
    container = Container(docker_config, docker_client)
    assert container._docker_client == docker_client


def test_init_without_docker_client(docker_config):
    with pytest.raises(RuntimeError, match="Docker is not running, or not configured."):
        Container(docker_config)


def test_validate_image_valid(docker_config, docker_client):
    container = Container(docker_config, docker_client)
    container._validate_image("alpine")


def test_validate_image_invalid(docker_config, docker_client):
    container = Container(docker_config, docker_client)
    with pytest.raises(ValueError, match='Image "invalid_image" is not allowed'):
        container._validate_image("invalid_image")


def test_create_container(docker_config, docker_client, volume):
    container = Container(docker_config, docker_client)
    container._create_container("alpine", 'echo "Hello, World!"', volume)
    docker_client.containers.run.assert_called_once_with(
        detach=True,
        image="alpine",
        network_mode=docker_config.network_mode,
        security_opt=docker_config.security_options,
        cap_drop=["ALL"],
        mem_limit=docker_config.limits.memory,
        volumes={"/host/path": {"bind": "/guest/path", "mode": "rw"}},
        command='echo "Hello, World!"',
    )


@pytest.mark.asyncio
async def test_run(docker_config, docker_client, volume):
    container = Container(docker_config, docker_client)
    on_create = AsyncMock()
    on_start = AsyncMock()
    on_finish = AsyncMock()

    container._create_container = MagicMock()
    mock_container = MagicMock()
    container._create_container.return_value = mock_container

    await container.run(
        image="alpine",
        command='echo "Hello, World!"',
        volume=volume,
        on_create=on_create,
        on_start=on_start,
        on_finish=on_finish,
    )

    on_create.assert_called_once()
    on_start.assert_called_once()
    mock_container.wait.assert_called_once()
    on_finish.assert_called_once()


@pytest.mark.asyncio
async def test_run_without_events(docker_config, docker_client, volume):
    container = Container(docker_config, docker_client)

    container._create_container = MagicMock()
    mock_container = MagicMock()
    container._create_container.return_value = mock_container

    await container.run(
        image="alpine",
        command='echo "Hello, World!"',
        volume=volume,
    )

    mock_container.wait.assert_called_once()
