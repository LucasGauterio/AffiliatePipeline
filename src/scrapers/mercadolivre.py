from src.scrapers.base import BaseScraper

class MercadoLivreScraper(BaseScraper):
    def scrape(self, keyword: str) -> list[dict]:
        # Mock implementation returning 3 products: cheap, medium, premium
        return [
            {
                "title": f"{keyword} - Mais Barato (Mock)",
                "price": "49.90",
                "link": "https://mercadolivre.com.br/afiliado-mock-barato",
                "store": "Mercado Livre"
            },
            {
                "title": f"{keyword} - Custo Benefício (Mock)",
                "price": "149.90",
                "link": "https://mercadolivre.com.br/afiliado-mock-medio",
                "store": "Mercado Livre"
            },
            {
                "title": f"{keyword} - Premium (Mock)",
                "price": "499.90",
                "link": "https://mercadolivre.com.br/afiliado-mock-caro",
                "store": "Mercado Livre"
            }
        ]
