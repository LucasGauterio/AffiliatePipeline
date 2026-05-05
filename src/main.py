import os
import sys

# Ensure src is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.secrets_manager import get_secret
from src.discovery import get_next_topic, mark_topic_as_done
from src.scrapers.mercadolivre import MercadoLivreScraper
from src.ai_generator import AIGenerator
from src.publisher import WordPressPublisher

def main():
    topic = get_next_topic()
    if not topic:
        print("Nenhuma pauta pendente.")
        return

    print(f"Iniciando pipeline para: {topic}")

    # Fetch secrets
    gemini_key = get_secret("GEMINI_API_KEY")
    wp_url = get_secret("WP_URL")
    wp_user = get_secret("WP_USER")
    wp_password = get_secret("WP_PASSWORD")

    # Scrape products
    scraper = MercadoLivreScraper()
    products = scraper.scrape(topic)

    # Generate content
    ai_gen = AIGenerator(gemini_key)
    post_data = ai_gen.generate_post(topic, products)

    # Publish
    publisher = WordPressPublisher(wp_url, wp_user, wp_password)
    result = publisher.publish(post_data, products)

    print(f"Post publicado com ID: {result.get('id')}")

    # Mark as done
    mark_topic_as_done(topic)

if __name__ == "__main__":
    main()
