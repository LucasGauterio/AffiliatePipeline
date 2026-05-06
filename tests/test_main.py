import pytest
from unittest.mock import patch, MagicMock
from src.main import main

@patch("src.main.get_secret")
@patch("src.main.get_next_topic")
@patch("src.main.mark_topic_as_done")
@patch("src.main.MercadoLivreScraper")
@patch("src.main.AmazonScraper")
@patch("src.main.AIGenerator")
@patch("src.main.StaticPublisher")
def test_main_success(
    mock_static_pub, 
    mock_ai_gen, 
    mock_amazon_scraper,
    mock_ml_scraper, 
    mock_mark_done, 
    mock_get_topic, 
    mock_get_secret
):
    # Setup secrets
    def fake_get_secret(key):
        return f"fake_{key}"
    mock_get_secret.side_effect = fake_get_secret

    # Setup topic
    mock_get_topic.return_value = "Fone de Ouvido"
    
    # Setup products
    mock_product_ml = {
        "title": "Fone MercadoLivre",
        "price": "59.90",
        "link": "http://ml",
        "image_url": "http://ml.jpg",
        "store": "Mercado Livre"
    }
    mock_product_am = {
        "title": "Fone Amazon",
        "price": "349.90",
        "link": "http://am",
        "image_url": "http://am.jpg",
        "store": "Amazon"
    }
    
    mock_ml_inst = MagicMock()
    mock_ml_inst.scrape.return_value = [mock_product_ml]
    mock_ml_scraper.return_value = mock_ml_inst
    
    mock_am_inst = MagicMock()
    mock_am_inst.scrape.return_value = [mock_product_am]
    mock_amazon_scraper.return_value = mock_am_inst
    
    # Setup generators
    mock_ai_inst = MagicMock()
    mock_ai_inst.generate_post.return_value = {"title": "Post Title", "content": "Post Content"}
    mock_ai_gen.return_value = mock_ai_inst
    
    # Setup publishers
    mock_static_inst = MagicMock()
    mock_static_inst.publish.return_value = {"slug": "post-title"}
    mock_static_pub.return_value = mock_static_inst
    
    # Run
    main()

    # Assertions
    mock_get_topic.assert_called_once()
    mock_ml_inst.scrape.assert_called_once_with("Fone de Ouvido")
    mock_am_inst.scrape.assert_called_once_with("Fone de Ouvido")
    
    # Verify curated product combination
    expected_am_product = dict(mock_product_am)
    expected_am_product["link"] = "http://am?tag=ehbom-20"
    expected_am_product["badge"] = "Custo-Benefício"

    curated_products = [
        dict(mock_product_ml, badge="Mais Barato"),
        expected_am_product
    ]
    
    mock_ai_inst.generate_post.assert_called_once_with("Fone de Ouvido", curated_products)
    mock_static_inst.publish.assert_called_once_with({"title": "Post Title", "content": "Post Content"}, curated_products)
    mock_mark_done.assert_called_once_with("Fone de Ouvido")

@patch("src.main.get_secret")
@patch("src.main.get_next_topic")
def test_main_no_topic(mock_get_topic, mock_get_secret):
    def fake_get_secret(key):
        return f"fake_{key}"
    mock_get_secret.side_effect = fake_get_secret
    mock_get_topic.return_value = None
    
    with patch("builtins.print") as mock_print:
        main()
        # Verify it printed the fallback empty message
        mock_print.assert_any_call("⚠️ Nenhuma pauta pendente ou tendência de produto qualificada encontrada hoje.")
