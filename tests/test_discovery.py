import os
import json
import pytest
from src.discovery import get_next_topic, mark_topic_as_done, get_google_trends, get_mercadolivre_trends

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

def test_get_google_trends_parsing(mocker):
    # Simulated Google Trends Daily RSS XML
    mock_rss_xml = """
    <rss version="2.0" xmlns:ht="http://google.com/trends">
        <channel>
            <item>
                <title>Garfídeo</title>
                <ht:approx_traffic>100,000+</ht:approx_traffic>
            </item>
            <item>
                <title>Fritadeira Sem Óleo</title>
                <ht:approx_traffic>50,000+</ht:approx_traffic>
            </item>
        </channel>
    </rss>
    """
    mock_response = mocker.Mock()
    mock_response.ok = True
    mock_response.content = mock_rss_xml.encode('utf-8')
    mocker.patch('requests.get', return_value=mock_response)
    
    trends = get_google_trends()
    assert trends == ["Garfídeo", "Fritadeira Sem Óleo"]

def test_get_mercadolivre_trends_parsing(mocker):
    # Simulated Mercado Livre Search trends API response
    mock_json_data = [
        {"keyword": "ventilador de teto", "url": "http://ml/ventilador"},
        {"keyword": "garrafa termica", "url": "http://ml/garrafa"}
    ]
    mock_response = mocker.Mock()
    mock_response.ok = True
    mock_response.json = lambda: mock_json_data
    mocker.patch('requests.get', return_value=mock_response)
    
    trends = get_mercadolivre_trends()
    assert trends == ["ventilador de teto", "garrafa termica"]

def test_get_next_topic_dynamic_ai(tmp_path, monkeypatch, mocker):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    monkeypatch.setenv("DATA_DIR", str(data_dir))
    
    # Mock XML and JSON requests
    google_response = mocker.Mock()
    google_response.ok = True
    google_response.content = b"<rss><channel><item><title>Aparelho de Fondue</title></item></channel></rss>"
    
    ml_response = mocker.Mock()
    ml_response.ok = True
    ml_response.json = lambda: [{"keyword": "panela eletrica"}]
    
    def side_effect(url, *args, **kwargs):
        if "google.com" in url:
            return google_response
        return ml_response
        
    mocker.patch('requests.get', side_effect=side_effect)
    
    # Mock Gemini AI model output
    mock_model = mocker.Mock()
    mock_generate_response = mocker.Mock()
    mock_generate_response.text = '{"topic": "Aparelho de Fondue Elétrico"}'
    mock_model.generate_content.return_value = mock_generate_response
    
    mocker.patch('google.generativeai.GenerativeModel', return_value=mock_model)
    mocker.patch('google.generativeai.configure')
    
    topic = get_next_topic(gemini_api_key="mock_key")
    assert topic == "Aparelho de Fondue Elétrico"
