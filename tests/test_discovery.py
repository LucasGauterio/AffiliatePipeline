import os
import json
import pytest
from src.discovery import get_next_topic, mark_topic_as_done

def test_get_next_topic_success(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    topics_file = data_dir / "topics.json"
    topics_file.write_text(json.dumps(["Topic A", "Topic B", "Topic C"]))
    history_file = data_dir / "history.json"
    history_file.write_text(json.dumps(["Topic A"]))
    monkeypatch.setenv("DATA_DIR", str(data_dir))
    assert get_next_topic() == "Topic B"

def test_get_next_topic_all_done(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    topics_file = data_dir / "topics.json"
    topics_file.write_text(json.dumps(["Topic A", "Topic B"]))
    history_file = data_dir / "history.json"
    history_file.write_text(json.dumps(["Topic A", "Topic B"]))
    monkeypatch.setenv("DATA_DIR", str(data_dir))
    assert get_next_topic() is None

def test_get_next_topic_no_history(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    topics_file = data_dir / "topics.json"
    topics_file.write_text(json.dumps(["Topic A", "Topic B"]))
    monkeypatch.setenv("DATA_DIR", str(data_dir))
    assert get_next_topic() == "Topic A"

def test_mark_topic_as_done(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    history_file = data_dir / "history.json"
    monkeypatch.setenv("DATA_DIR", str(data_dir))
    mark_topic_as_done("Topic A")
    assert json.loads(history_file.read_text()) == ["Topic A"]
    mark_topic_as_done("Topic B")
    assert json.loads(history_file.read_text()) == ["Topic A", "Topic B"]
