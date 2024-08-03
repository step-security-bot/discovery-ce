from unittest.mock import Mock, patch

import pytest
import requests

from discovery.utils import validate_domain


@pytest.fixture
def mock_response():
    mock_resp = Mock()
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.return_value = {
        "Status": 0,
        "Answer": [{"data": "93.184.216.34"}],
    }
    return mock_resp


def test_validate_domain_success(mock_response):
    with patch("requests.get", return_value=mock_response):
        assert validate_domain("example.com")


def test_validate_domain_invalid_pattern():
    assert not validate_domain("invalid_domain")


def test_validate_domain_dns_status_failure():
    mock_resp = Mock()
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.return_value = {"Status": 3}  # Non-zero status indicates DNS failure
    with patch("requests.get", return_value=mock_resp):
        assert not validate_domain("example.com")


def test_validate_domain_no_answer():
    mock_resp = Mock()
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.return_value = {"Status": 0, "Answer": []}
    with patch("requests.get", return_value=mock_resp):
        assert not validate_domain("example.com")


def test_validate_domain_ip_not_global():
    mock_resp = Mock()
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.return_value = {"Status": 0, "Answer": [{"data": "192.168.1.1"}]}
    with patch("requests.get", return_value=mock_resp):
        assert not validate_domain("example.com")


def test_validate_domain_connection_error():
    with patch("requests.get", side_effect=requests.exceptions.ConnectionError):
        assert not validate_domain("example.com")


def test_validate_domain_http_error():
    with patch("requests.get", side_effect=requests.exceptions.HTTPError):
        assert not validate_domain("example.com")
