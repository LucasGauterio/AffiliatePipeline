import pytest
from src.scrapers.base import BaseScraper

def test_base_scraper_is_abstract():
    with pytest.raises(TypeError):
        # Should raise TypeError because it's an abstract class
        scraper = BaseScraper()

def test_base_scraper_abstract_methods():
    class DummyScraper(BaseScraper):
        pass

    with pytest.raises(TypeError):
        # Should raise TypeError because it doesn't implement abstract methods
        scraper = DummyScraper()

    class ValidScraper(BaseScraper):
        def scrape(self, keyword: str) -> list[dict]:
            return [{"title": "Dummy", "price": "10", "link": "http", "store": "Dummy"}]

    # Should not raise
    valid_scraper = ValidScraper()
    assert valid_scraper.scrape("test") == [{"title": "Dummy", "price": "10", "link": "http", "store": "Dummy"}]
