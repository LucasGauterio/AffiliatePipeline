import pytest
from src.scrapers.mercadolivre import MercadoLivreScraper

def test_mercadolivre_scraper_mock():
    scraper = MercadoLivreScraper()
    results = scraper.scrape("Fone de Ouvido")

    assert isinstance(results, list)
    assert len(results) == 3

    # Check structure
    for item in results:
        assert "title" in item
        assert "price" in item
        assert "link" in item
        assert "store" in item
        assert item["store"] == "Mercado Livre"
        
        # In mock mode, we expect the keyword to be part of the title
        assert "Fone de Ouvido" in item["title"]

    # In our specific rules, we want 3 items representing: cheap, medium, premium
    prices = [float(item["price"]) for item in results]
    assert prices[0] < prices[1] < prices[2]
