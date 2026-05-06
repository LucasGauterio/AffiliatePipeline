import json
import datetime
import google.generativeai as genai

class AIGenerator:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def generate_post(self, keyword: str, products: list[dict]) -> dict:
        """
        Generates a blog post using Gemini.

        Args:
            keyword: The main topic/keyword
            products: List of products scraped from stores

        Returns:
            dict: Containing 'title' and 'content' keys
        """
        current_year = datetime.datetime.now().year
        prompt = f"""
        You are an expert affiliate marketing copywriter specializing in the Brazilian e-commerce market.
        Write a product review post in Portuguese about {keyword}.
        Here are the products to compare:
        {json.dumps(products, indent=2, ensure_ascii=False)}

        CRITICAL REQUIREMENT:
        - You MUST refer strictly to the current year {current_year} for any recommendations, dates, guides, or listings.
        - NEVER mention past years like 2024, 2025, or any other year. Everything must feel highly relevant for {current_year}.

        You must return ONLY a JSON object with this exact format, with no markdown code blocks:
        {{
            "title": "A catchy title for the post (mentioning {current_year} if appropriate)",
            "content": "The full HTML content of the post including <h2> tags for sections."
        }}
        """

        response = self.model.generate_content(prompt)
        text = response.text

        # Clean markdown formatting if present
        text = text.replace('```json', '').replace('```', '').strip()

        # Bulletproof fail-safe: Replace any past years with the current year
        for past_year in range(2020, current_year):
            text = text.replace(str(past_year), str(current_year))

        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse Gemini response as JSON: {text}") from e

    def generate_fallback_products(self, keyword: str) -> list[dict]:
        """
        Generates realistic, high-quality real-world trending products for a keyword when scrapers are blocked.
        Provides beautiful high-res image URLs (e.g., from Unsplash) to guarantee stunning presentation.
        """
        current_year = datetime.datetime.now().year
        prompt = f"""
        Você é um assistente de e-commerce e especialista em marketing de afiliados no mercado brasileiro.
        Dado o termo de busca de categoria '{keyword}', gere exatamente 3 produtos físicos reais e populares que existam de verdade no mercado brasileiro para esta categoria, representando três segmentos:
        1. "Mais Barato" (Opção de entrada de boa qualidade)
        2. "Custo-Benefício" (Melhor relação preço/performance)
        3. "Premium" (Opção de alta gama/luxo)

        CRITICAL REQUIREMENT:
        - Se fizer qualquer menção a ano ou guias no título, use estritamente o ano atual de {current_year}. NUNCA use anos passados como 2024 ou 2025.

        Para cada produto, forneça:
        - title: Nome completo e exato do modelo do produto em português (ex: "Fritadeira Elétrica Air Fryer Mondial AF-31")
        - price: Preço realista em reais como uma string flutuante (ex: "349.90")
        - link: Um link de pesquisa real simplificado na Amazon ou Mercado Livre (ex: "https://www.amazon.com.br/s?k=air+fryer+mondial")
        - image_url: Uma URL de imagem de alta qualidade do Unsplash que corresponda visualmente a este produto ou categoria para ficar impecável no design (ex: "https://images.unsplash.com/photo-1588854337236-6889d631faa8?w=600&q=80")
        - store: A loja onde é mais famoso ("Amazon" ou "Mercado Livre")
        - badge: "Mais Barato", "Custo-Benefício" ou "Premium" (exatamente estes valores)

        Você deve retornar APENAS uma lista JSON com o formato exato abaixo, sem blocos de código markdown (```json ... ```):
        [
          {{
            "title": "Título completo do produto",
            "price": "349.90",
            "link": "https://...",
            "image_url": "https://images.unsplash.com/...",
            "store": "Amazon",
            "badge": "Mais Barato"
          }},
          ...
        ]
        """
        response = self.model.generate_content(prompt)
        text = response.text.replace('```json', '').replace('```', '').strip()

        # Bulletproof fail-safe: Replace any past years with the current year
        for past_year in range(2020, current_year):
            text = text.replace(str(past_year), str(current_year))

        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse fallback products JSON: {text}") from e
