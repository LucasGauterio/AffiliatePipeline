import re
import requests
from bs4 import BeautifulSoup
from src.scrapers.base import BaseScraper

class AmazonScraper(BaseScraper):
    def scrape(self, keyword: str) -> list[dict]:
        """
        Scrapes real products from Amazon.com.br search results.
        Uses advanced user-agents to avoid simple anti-bot redirects.
        
        Args:
            keyword: The search term (e.g. "Fone de Ouvido Bluetooth")
            
        Returns:
            list[dict]: Curated list of 3 products (Barato, Custo-Beneficio, Premium)
        """
        print(f"🛒 [Amazon] Buscando produtos reais para: '{keyword}'...")
        encoded_keyword = requests.utils.quote(keyword)
        url = f"https://www.amazon.com.br/s?k={encoded_keyword}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://www.google.com/",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive"
        }
        
        try:
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 503 or "api-services-support@amazon.com" in res.text:
                print("⚠️ [Amazon] Bloqueio ou CAPTCHA detectado. Retornando lista vazia.")
                return []
                
            if not res.ok:
                print(f"⚠️ [Amazon] Falha na requisição: HTTP {res.status_code}")
                return []
                
            soup = BeautifulSoup(res.text, "html.parser")
            items = soup.select('div[data-component-type="s-search-result"]')
            
            valid_products = []
            for item in items:
                # 1. Title
                title_el = item.select_one('h2 a span')
                if not title_el:
                    continue
                title = title_el.get_text().strip()
                
                # 2. Link
                link_el = item.select_one('h2 a')
                if not link_el or not link_el.get('href'):
                    continue
                link = link_el.get('href')
                if link.startswith('/'):
                    link = "https://www.amazon.com.br" + link
                    
                # Clean affiliate parameters or other search trackers
                if "?" in link:
                    link = link.split("?")[0]
                    
                # 3. Image URL
                img_el = item.select_one('img.s-image')
                image_url = img_el.get('src') if img_el else ""
                
                # 4. Price
                price_el = item.select_one('span.a-price span.a-offscreen')
                if not price_el:
                    price_el = item.select_one('span.a-price')
                    
                if not price_el:
                    continue
                    
                price_text = price_el.get_text().strip()
                
                # Parse localized currency pattern (e.g. "R$ 1.549,90" or "R$49,90")
                price_nums = re.findall(r'[\d\.,]+', price_text)
                if not price_nums:
                    continue
                    
                # Standardize decimals and thousands (Brazilian format: 1.500,00 -> 1500.00)
                price_str = price_nums[0].replace(".", "").replace(",", ".")
                try:
                    price = float(price_str)
                except ValueError:
                    continue
                    
                # Filter out small accessory listings (less than R$ 15.0)
                if price < 15.0:
                    continue
                    
                valid_products.append({
                    "title": title,
                    "price": f"{price:.2f}",
                    "link": link,
                    "image_url": image_url,
                    "store": "Amazon"
                })
                
            if len(valid_products) < 3:
                print(f"⚠️ [Amazon] Apenas {len(valid_products)} produtos válidos encontrados (mínimo de 3 necessário).")
                return valid_products
                
            # Sort by price ascending
            valid_products.sort(key=lambda x: float(x["price"]))
            
            # Select three representatives
            cheap = valid_products[0]
            cheap["badge"] = "Mais Barato"
            
            mid_idx = len(valid_products) // 2
            value = valid_products[mid_idx]
            value["badge"] = "Custo-Benefício"
            
            premium_idx = min(len(valid_products) - 1, int(len(valid_products) * 0.90))
            if premium_idx <= mid_idx:
                premium_idx = len(valid_products) - 1
            premium = valid_products[premium_idx]
            premium["badge"] = "Premium"
            
            print(f"✅ [Amazon] 3 produtos reais selecionados com sucesso!")
            return [cheap, value, premium]
            
        except Exception as e:
            print(f"⚠️ [Amazon] Exceção durante busca: {e}")
            return []
