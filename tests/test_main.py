import pytest
from unittest.mock import patch, MagicMock
from src.main import main

@patch("src.main.get_secret")
@patch("src.main.get_next_topic")
@patch("src.main.mark_topic_as_done")
@patch("src.main.MercadoLivreScraper")
@patch("src.main.AIGenerator")
@patch("src.main.WordPressPublisher")
def test_main_success(
    mock_wp_pub, 
    mock_ai_gen, 
    mock_scraper, 
    mock_mark_done, 
    mock_get_topic, 
    mock_get_secret
):
    # Setup mocks
    mock_get_topic.return_value = "Fone de Ouvido"
    
    mock_scraper_inst = MagicMock()
    mock_scraper_inst.scrape.return_value = [{"title": "Mock Product"}]
    mock_scraper.return_value = mock_scraper_inst
    
    mock_ai_inst = MagicMock()
    mock_ai_inst.generate_post.return_value = {"title": "Post Title", "content": "Post Content"}
    mock_ai_gen.return_value = mock_ai_inst
    
    mock_wp_inst = MagicMock()
    mock_wp_inst.publish.return_value = {"id": 1}
    mock_wp_pub.return_value = mock_wp_inst
    
    def fake_get_secret(key):
        return f"fake_{key}"
    mock_get_secret.side_effect = fake_get_secret

    # Run
    main()

    # Assertions
    mock_get_topic.assert_called_once()
    mock_scraper_inst.scrape.assert_called_once_with("Fone de Ouvido")
    mock_ai_inst.generate_post.assert_called_once_with("Fone de Ouvido", [{"title": "Mock Product"}])
    mock_wp_inst.publish.assert_called_once_with({"title": "Post Title", "content": "Post Content"}, [{"title": "Mock Product"}])
    mock_mark_done.assert_called_once_with("Fone de Ouvido")

@patch("src.main.get_next_topic")
def test_main_no_topic(mock_get_topic):
    mock_get_topic.return_value = None
    
    with patch("builtins.print") as mock_print:
        main()
        mock_print.assert_called_with("Nenhuma pauta pendente.")
