import pytest
from src.scrapers.amazon import AmazonScraper

def test_amazon_scraper_mock():
    scraper = AmazonScraper()
    results = scraper.scrape("Mouse sem Fio")

    assert isinstance(results, list)
    assert len(results) == 3

    # Check structure
    for item in results:
        assert "title" in item
        assert "price" in item
        assert "link" in item
        assert "store" in item
        assert item["store"] == "Amazon"
        
        # In mock mode, we expect the keyword to be part of the title
        assert "Mouse sem Fio" in item["title"]

    prices = [float(item["price"]) for item in results]
    assert prices[0] < prices[1] < prices[2]
