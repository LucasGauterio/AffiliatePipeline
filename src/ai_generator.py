import json
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
        prompt = f"""
        You are an expert affiliate marketing copywriter.
        Write a blog post about {keyword}.
        Here are the products to compare:
        {json.dumps(products, indent=2, ensure_ascii=False)}

        You must return ONLY a JSON object with this exact format, with no markdown code blocks:
        {{
            "title": "A catchy title for the post",
            "content": "The full HTML content of the post including <h2> tags for sections."
        }}
        """

        response = self.model.generate_content(prompt)
        text = response.text

        # Clean markdown formatting if present
        text = text.replace('```json', '').replace('```', '').strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse Gemini response as JSON: {text}") from e
