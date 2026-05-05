from src.scrapers.base import BaseScraper

class AmazonScraper(BaseScraper):
    def scrape(self, keyword: str) -> list[dict]:
        # Mock implementation returning 3 products: cheap, medium, premium
        return [
            {
                "title": f"{keyword} - Básica (Mock)",
                "price": "35.90",
                "link": "https://amazon.com.br/afiliado-mock-barato",
                "store": "Amazon"
            },
            {
                "title": f"{keyword} - Intermediário (Mock)",
                "price": "120.50",
                "link": "https://amazon.com.br/afiliado-mock-medio",
                "store": "Amazon"
            },
            {
                "title": f"{keyword} - High-End (Mock)",
                "price": "399.00",
                "link": "https://amazon.com.br/afiliado-mock-caro",
                "store": "Amazon"
            }
        ]
