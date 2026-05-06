import os
import sys

# Ensure src is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.secrets_manager import get_secret
from src.discovery import get_next_topic, mark_topic_as_done
from src.scrapers.mercadolivre import MercadoLivreScraper
from src.scrapers.amazon import AmazonScraper
from src.ai_generator import AIGenerator
from src.publisher import StaticPublisher

def main():
    # Fetch secrets or use local .env fallbacks
    gemini_key = get_secret("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    posts_json_path = get_secret("POSTS_JSON_PATH") or os.getenv("POSTS_JSON_PATH", "storefront/public/data/posts.json")

    if not gemini_key:
        print("❌ Erro crítico: GEMINI_API_KEY não encontrada nos segredos ou variáveis de ambiente.")
        sys.exit(1)

    # 1. Discover Topic (AI-curated Trends with local fallback)
    topic = get_next_topic(gemini_key)
    if not topic:
        print("⚠️ Nenhuma pauta pendente ou tendência de produto qualificada encontrada hoje.")
        return

    print(f"🏁 Iniciando pipeline automatizada para a pauta: '{topic}'")

    # 2. Scrape Products from both partner platforms
    ml_products = []
    am_products = []
    
    try:
        ml_products = MercadoLivreScraper().scrape(topic)
    except Exception as e:
        print(f"⚠️ Erro no scraper do Mercado Livre: {e}")
        
    try:
        am_products = AmazonScraper().scrape(topic)
    except Exception as e:
        print(f"⚠️ Erro no scraper da Amazon: {e}")
        
    # Combine results and verify
    all_products = ml_products + am_products
    if not all_products:
        print("❌ Falha crítica: Nenhum produto pôde ser coletado das lojas parceiras.")
        return
        
    # 3. Smart Curation & Merging across platforms
    if len(all_products) >= 3:
        # Sort combined results by price ascending
        all_products.sort(key=lambda x: float(x["price"]))
        
        # Select the best 3 representing the segments
        cheap = all_products[0]
        cheap["badge"] = "Mais Barato"
        
        mid_idx = len(all_products) // 2
        value = all_products[mid_idx]
        value["badge"] = "Custo-Benefício"
        
        # Get the highest-priced item from the list
        premium = all_products[-1]
        premium["badge"] = "Premium"
        
        products = [cheap, value, premium]
    else:
        # If fewer than 3 items overall, use whatever we gathered
        products = all_products
        for i, badge in enumerate(["Mais Barato", "Custo-Benefício", "Premium"]):
            if i < len(products):
                products[i]["badge"] = badge

    print("📦 Produtos curados e selecionados para a vitrine:")
    for p in products:
        print(f"  - [{p['store']}] {p['badge']}: {p['title']} - R$ {p['price']}")

    # 4. Generate AI Comparison content using Gemini
    print("🤖 Gerando análise comparativa técnica profunda com Gemini...")
    ai_gen = AIGenerator(gemini_key)
    post_data = ai_gen.generate_post(topic, products)

    # 5. Publish to Static JSON database
    print(f"💾 Gravando post estruturado em: {posts_json_path}")
    publisher = StaticPublisher(json_path=posts_json_path)
    result = publisher.publish(post_data, products)

    print(f"🚀 Post publicado com sucesso! Slug gerado: {result.get('slug')}")

    # 6. Mark as completed
    mark_topic_as_done(topic)
    print("🎯 Pipeline finalizada com sucesso!")

if __name__ == "__main__":
    main()
