import pytest
from unittest.mock import patch, MagicMock
from src.ai_generator import AIGenerator

@patch("src.ai_generator.genai")
def test_ai_generator_success(mock_genai):
    # Setup mock
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.text = '{"title": "Melhores Fones Bluetooth de 2026", "content": "<h2>Introdução</h2><p>Mocked content</p>"}'
    mock_model.generate_content.return_value = mock_response
    mock_genai.GenerativeModel.return_value = mock_model

    generator = AIGenerator(api_key="mocked_key")
    result = generator.generate_post(
        keyword="Fone Bluetooth",
        products=[{"title": "Fone 1", "price": "10", "link": "http", "store": "ML"}]
    )

    assert "title" in result
    assert "content" in result
    assert result["title"] == "Melhores Fones Bluetooth de 2026"
    assert "Mocked content" in result["content"]

    # Check if generate_content was called
    mock_model.generate_content.assert_called_once()
    
@patch("src.ai_generator.genai")
def test_ai_generator_json_parse_error(mock_genai):
    # Setup mock to return invalid JSON
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.text = 'invalid json response'
    mock_model.generate_content.return_value = mock_response
    mock_genai.GenerativeModel.return_value = mock_model

    generator = AIGenerator(api_key="mocked_key")
    with pytest.raises(ValueError, match="Failed to parse Gemini response as JSON"):
        generator.generate_post(keyword="Fone", products=[])
