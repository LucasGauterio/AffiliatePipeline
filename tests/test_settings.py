import os
import pytest
from config.settings import AppSettings

def test_settings_loads_env_vars(monkeypatch):
    monkeypatch.setenv("ENV", "production")
    monkeypatch.setenv("GCP_PROJECT_ID", "test-project-123")
    settings = AppSettings()
    assert settings.ENV == "production"
    assert settings.GCP_PROJECT_ID == "test-project-123"

def test_settings_default_values(monkeypatch):
    monkeypatch.delenv("ENV", raising=False)
    monkeypatch.delenv("GCP_PROJECT_ID", raising=False)
    settings = AppSettings()
    assert settings.ENV == "development"
    assert settings.GCP_PROJECT_ID is None
