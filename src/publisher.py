import requests
import bleach

class WordPressPublisher:
    def __init__(self, wp_url: str, wp_user: str, wp_password: str):
        self.wp_url = wp_url.rstrip("/")
        self.wp_user = wp_user
        self.wp_password = wp_password

    def _sanitize_content(self, html_content: str) -> str:
        """
        Sanitizes the HTML content to prevent XSS attacks.
        """
        allowed_tags = [
            'a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
            'em', 'i', 'li', 'ol', 'strong', 'ul', 'p', 'h1', 'h2', 'h3',
            'h4', 'h5', 'h6', 'br', 'hr', 'img', 'span', 'div', 'table',
            'thead', 'tbody', 'tr', 'th', 'td'
        ]
        allowed_attrs = {
            '*': ['class', 'id', 'style'],
            'a': ['href', 'title', 'target', 'rel'],
            'img': ['src', 'alt', 'width', 'height']
        }
        return bleach.clean(
            html_content,
            tags=allowed_tags,
            attributes=allowed_attrs,
            strip=True
        )

    def _create_payload(self, post_data: dict, products: list[dict]) -> dict:
        acf_data = {}
        for i, product in enumerate(products, start=1):
            acf_data[f"product_{i}_title"] = product["title"]
            acf_data[f"product_{i}_price"] = product["price"]
            acf_data[f"product_{i}_link"] = product["link"]
            acf_data[f"product_{i}_image"] = product.get("image_url", "")
            acf_data[f"product_{i}_store"] = product["store"]

        return {
            "title": post_data["title"],
            "content": self._sanitize_content(post_data["content"]),
            "status": "publish",
            "comment_status": "closed",
            "ping_status": "closed",
            "acf": acf_data
        }

    def publish(self, post_data: dict, products: list[dict]) -> dict:
        """
        Publishes the post to WordPress.
        """
        payload = self._create_payload(post_data, products)
        endpoint = f"{self.wp_url}/index.php/wp-json/wp/v2/posts"
        
        response = requests.post(
            endpoint,
            json=payload,
            auth=(self.wp_user, self.wp_password)
        )
        response.raise_for_status()
        return response.json()
