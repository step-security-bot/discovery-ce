import base64

import pytest

from discovery.containers.volume import ContainerVolume, Mode


@pytest.fixture
def base_path(tmp_path):
    return str(tmp_path)


@pytest.fixture
def container_volume(base_path):
    return ContainerVolume(
        base_path=base_path, mode=Mode.READ_WRITE, change_owner=False
    )


def test_create_volume(container_volume):
    assert container_volume._volume_path.exists()
    assert container_volume._volume_path.is_dir()


def test_write_file(container_volume):
    path = "testfile.txt"
    content = "Hello, World!"
    container_volume.write(path, content)
    assert (container_volume._volume_path / path).exists()
    with open(container_volume._volume_path / path) as file:
        assert file.read() == content


def test_read_file(container_volume):
    path = "testfile.txt"
    content = "Hello, World!"
    with open(container_volume._volume_path / path, "w") as file:
        file.write(content)
    read_content = container_volume.read(path)
    assert read_content == content


def test_read_file_bytes(container_volume):
    path = "testfile.txt"
    content = b"Hello, Bytes!"
    with open(container_volume._volume_path / path, "wb") as file:
        file.write(content)
    read_content = container_volume.read(path, read_bytes=True)
    assert read_content == content


def test_make_dir(container_volume):
    dir_name = "testdir"
    container_volume.make_dir(dir_name)
    assert (container_volume._volume_path / dir_name).exists() is True
    assert (container_volume._volume_path / dir_name).is_dir() is True


def test_file_exists(container_volume):
    path = "testfile.txt"
    content = "Hello, World!"
    container_volume.write(path, content)
    assert container_volume.file_exists(path) is True
    assert container_volume.file_exists("non_existent_file.txt") is False


def test_files(container_volume):
    file_path = "file.txt"
    file_content = "file content"
    with open(container_volume._volume_path / file_path, "w") as file:
        file.write(file_content)

    files = container_volume.files
    assert any(file.name == file_path for file in files)
    encoded_content = base64.b64encode(file_content.encode()).decode()
    assert any(file.content == encoded_content for file in files)


def test_mount(container_volume):
    volume = container_volume.mount()
    assert volume.host == str(container_volume._volume_path)
    assert volume.guest == str(container_volume._volume_path)
    assert volume.mode == Mode.READ_WRITE


def test_cleanup(container_volume):
    container_volume.cleanup()
    assert not container_volume._volume_path.exists()
