import pytest
from unittest.mock import patch, MagicMock
from config.secrets_manager import get_secret

@patch("config.secrets_manager.secretmanager.SecretManagerServiceClient")
def test_get_secret_production(mock_client_class, monkeypatch):
    monkeypatch.setenv("ENV", "production")
    monkeypatch.setenv("GCP_PROJECT_ID", "my-project")
    mock_client = mock_client_class.return_value
    mock_response = MagicMock()
    mock_response.payload.data.decode.return_value = "secret-value"
    mock_client.access_secret_version.return_value = mock_response
    secret = get_secret("MY_SECRET")
    assert secret == "secret-value"
    mock_client.access_secret_version.assert_called_once_with(
        request={"name": "projects/my-project/secrets/MY_SECRET/versions/latest"}
    )

def test_get_secret_local(monkeypatch):
    monkeypatch.setenv("ENV", "development")
    monkeypatch.setenv("MY_SECRET", "local-secret")
    secret = get_secret("MY_SECRET")
    assert secret == "local-secret"

def test_get_secret_local_missing(monkeypatch):
    monkeypatch.setenv("ENV", "development")
    monkeypatch.delenv("MISSING_SECRET", raising=False)
    with pytest.raises(ValueError, match="Secret MISSING_SECRET not found"):
        get_secret("MISSING_SECRET")
