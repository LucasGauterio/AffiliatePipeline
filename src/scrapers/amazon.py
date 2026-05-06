from src.scrapers.base import BaseScraper

class AmazonScraper(BaseScraper):
    def scrape(self, keyword: str) -> list[dict]:
        # Mock implementation returning 3 products: cheap, medium, premium
        return [
            {
                "title": f"{keyword} - Básica (Mock)",
                "price": "35.90",
                "link": "https://amazon.com.br/afiliado-mock-barato",
                "image_url": "https://via.placeholder.com/300x300.png?text=Amazon+Basica",
                "store": "Amazon"
            },
            {
                "title": f"{keyword} - Intermediário (Mock)",
                "price": "120.50",
                "link": "https://amazon.com.br/afiliado-mock-medio",
                "image_url": "https://via.placeholder.com/300x300.png?text=Amazon+Intermediario",
                "store": "Amazon"
            },
            {
                "title": f"{keyword} - High-End (Mock)",
                "price": "399.00",
                "link": "https://amazon.com.br/afiliado-mock-caro",
                "image_url": "https://via.placeholder.com/300x300.png?text=Amazon+Premium",
                "store": "Amazon"
            }
        ]
