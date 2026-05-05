from abc import ABC, abstractmethod

class BaseScraper(ABC):
    """
    Abstract base class for all scrapers (Amazon, MercadoLivre, etc.)
    """

    @abstractmethod
    def scrape(self, keyword: str) -> list[dict]:
        """
        Scrapes products for a given keyword.

        Args:
            keyword (str): The search term (e.g. "Fone de Ouvido Bluetooth")

        Returns:
            list[dict]: A list of product dictionaries containing:
                - title (str)
                - price (str)
                - link (str)
                - store (str)
        """
        pass
