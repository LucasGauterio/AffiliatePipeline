import os
import json
import re
import unicodedata
from datetime import datetime
import bleach

class StaticPublisher:
    def __init__(self, json_path: str = None):
        if json_path is None:
            # Default to storefront assets public folder
            self.json_path = os.getenv(
                "POSTS_JSON_PATH", 
                os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "storefront", "public", "data", "posts.json"))
            )
        else:
            self.json_path = json_path

    def _slugify(self, text: str) -> str:
        """
        Generates a clean, URL-safe slug from input text.
        Converts to lowercase, removes accents, and replaces non-alphanumeric chars with hyphens.
        """
        # Normalize to strip accents
        n_text = unicodedata.normalize('NFKD', text)
        clean_text = n_text.encode('ASCII', 'ignore').decode('utf-8')
        # Lowercase and replace symbols
        slug = clean_text.lower()
        slug = re.sub(r'[^a-z0-9]+', '-', slug)
        return slug.strip('-')

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

    def _read_posts(self) -> list[dict]:
        """
        Reads existing posts list from either GCS or local file system.
        """
        posts = []
        if self.json_path.startswith("gs://"):
            from google.cloud import storage
            try:
                parts = self.json_path[5:].split("/", 1)
                bucket_name = parts[0]
                blob_name = parts[1]
                
                client = storage.Client()
                bucket = client.bucket(bucket_name)
                blob = bucket.blob(blob_name)
                
                if blob.exists():
                    content = blob.download_as_text(encoding='utf-8')
                    posts = json.loads(content)
            except Exception as e:
                print(f"Error reading from GCS: {e}. Returning empty list.")
                posts = []
        else:
            if os.path.exists(self.json_path):
                try:
                    with open(self.json_path, 'r', encoding='utf-8') as f:
                        posts = json.load(f)
                except Exception as e:
                    print(f"Error reading local file: {e}. Returning empty list.")
                    posts = []
        return posts

    def _write_posts(self, posts: list[dict]):
        """
        Writes posts list to either GCS or local file system.
        """
        if self.json_path.startswith("gs://"):
            from google.cloud import storage
            parts = self.json_path[5:].split("/", 1)
            bucket_name = parts[0]
            blob_name = parts[1]
            
            client = storage.Client()
            bucket = client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            
            content = json.dumps(posts, ensure_ascii=False, indent=2)
            blob.upload_from_string(content, content_type='application/json')
        else:
            # Local filesystem
            os.makedirs(os.path.dirname(self.json_path), exist_ok=True)
            with open(self.json_path, 'w', encoding='utf-8') as f:
                json.dump(posts, f, ensure_ascii=False, indent=2)

    def publish(self, post_data: dict, products: list[dict]) -> dict:
        """
        Publishes the product comparison post statically.
        """
        slug = self._slugify(post_data["title"])
        sanitized_content = self._sanitize_content(post_data["content"])

        # Map products with categories (badges)
        badges = ["Mais Barato", "Custo-Benefício", "Premium"]
        structured_products = []
        for i, product in enumerate(products[:3]):
            structured_products.append({
                "title": product["title"],
                "price": product["price"],
                "link": product["link"],
                "image_url": product.get("image_url", ""),
                "store": product["store"],
                "badge": badges[i] if i < len(badges) else "Recomendado"
            })

        post_item = {
            "slug": slug,
            "title": post_data["title"],
            "content": sanitized_content,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "products": structured_products
        }

        # Transactional read-modify-write
        posts = self._read_posts()

        updated = False
        for idx, existing_post in enumerate(posts):
            if existing_post["slug"] == slug:
                posts[idx] = post_item
                updated = True
                break

        if not updated:
            posts.append(post_item)

        self._write_posts(posts)
        return post_item
