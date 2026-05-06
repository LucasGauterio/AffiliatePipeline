import os
import sys

# Ensure src is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.secrets_manager import get_secret
from src.discovery import get_next_topic, mark_topic_as_done
from src.scrapers.mercadolivre import MercadoLivreScraper
from src.ai_generator import AIGenerator
from src.publisher import StaticPublisher

def main():
    topic = get_next_topic()
    if not topic:
        print("Nenhuma pauta pendente.")
        return

    print(f"Iniciando pipeline para: {topic}")

    # Fetch secrets
    gemini_key = get_secret("GEMINI_API_KEY")
    posts_json_path = get_secret("POSTS_JSON_PATH")

    # Scrape products
    scraper = MercadoLivreScraper()
    products = scraper.scrape(topic)

    # Generate content
    ai_gen = AIGenerator(gemini_key)
    post_data = ai_gen.generate_post(topic, products)

    # Publish
    publisher = StaticPublisher(json_path=posts_json_path)
    result = publisher.publish(post_data, products)

    print(f"Post publicado com slug: {result.get('slug')}")

    # Mark as done
    mark_topic_as_done(topic)

if __name__ == "__main__":
    main()
