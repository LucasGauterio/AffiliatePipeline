import requests
from src.scrapers.base import BaseScraper

class MercadoLivreScraper(BaseScraper):
    def scrape(self, keyword: str) -> list[dict]:
        """
        Scrapes real products from Mercado Livre's public search API.
        
        Args:
            keyword: The search term (e.g. "Fone de Ouvido Bluetooth")
            
        Returns:
            list[dict]: Curated list of 3 products (Barato, Custo-Beneficio, Premium)
        """
        print(f"🛒 [Mercado Livre] Buscando produtos reais para: '{keyword}'...")
        encoded_keyword = requests.utils.quote(keyword)
        url = f"https://api.mercadolibre.com/sites/MLB/search?q={encoded_keyword}"
        
        try:
            res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            if not res.ok:
                print(f"⚠️ [Mercado Livre] Falha ao conectar: HTTP {res.status_code}")
                return []
                
            data = res.json()
            results = data.get("results", [])
            if not results:
                print("⚠️ [Mercado Livre] Nenhum produto encontrado.")
                return []
                
            valid_products = []
            for item in results:
                title = item.get("title")
                price_val = item.get("price")
                permalink = item.get("permalink")
                thumbnail = item.get("secure_thumbnail") or item.get("thumbnail")
                
                if not title or price_val is None or not permalink:
                    continue
                    
                price = float(price_val)
                # Filter out accessories / low-cost noise (R$ 15 threshold)
                if price < 15.0:
                    continue
                    
                # Upgrade thumbnail quality to high-resolution original (-O.jpg)
                if thumbnail:
                    for suffix in ["-I.jpg", "-V.jpg", "-X.jpg", "-O.jpg"]:
                        if suffix in thumbnail and suffix != "-O.jpg":
                            thumbnail = thumbnail.replace(suffix, "-O.jpg")
                            break
                
                valid_products.append({
                    "title": title,
                    "price": f"{price:.2f}",
                    "link": permalink,
                    "image_url": thumbnail or "",
                    "store": "Mercado Livre"
                })
                
            if len(valid_products) < 3:
                print(f"⚠️ [Mercado Livre] Apenas {len(valid_products)} produtos válidos encontrados (mínimo de 3 necessário).")
                return valid_products
                
            # Sort by price ascending
            valid_products.sort(key=lambda x: float(x["price"]))
            
            # Smart Curated Selection
            # 1. Mais Barato (Cheapest)
            cheap = valid_products[0]
            cheap["badge"] = "Mais Barato"
            
            # 2. Custo-Benefício (Median)
            mid_idx = len(valid_products) // 2
            value = valid_products[mid_idx]
            value["badge"] = "Custo-Benefício"
            
            # 3. Premium (90th percentile to filter outliers or incorrect pricing listings)
            premium_idx = min(len(valid_products) - 1, int(len(valid_products) * 0.90))
            if premium_idx <= mid_idx:
                premium_idx = len(valid_products) - 1
            premium = valid_products[premium_idx]
            premium["badge"] = "Premium"
            
            print(f"✅ [Mercado Livre] 3 produtos reais selecionados com sucesso!")
            return [cheap, value, premium]
            
        except Exception as e:
            print(f"⚠️ [Mercado Livre] Exceção durante busca: {e}")
            return []
