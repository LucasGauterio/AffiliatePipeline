import os
import json
import xml.etree.ElementTree as ET
import requests
import google.generativeai as genai

def get_data_dir():
    return os.getenv("DATA_DIR", os.path.join(os.path.dirname(__file__), "..", "data"))

def get_google_trends() -> list[str]:
    """
    Fetches daily hot searches in Brazil from Google Trends Daily RSS.
    """
    url = "https://trends.google.com.br/trends/trendingsearches/daily/rss?geo=BR"
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8"
        }
        res = requests.get(url, headers=headers, timeout=10)
        if res.ok:
            root = ET.fromstring(res.content)
            titles = []
            for item in root.findall(".//item"):
                title = item.find("title")
                if title is not None and title.text:
                    titles.append(title.text.strip())
            return titles
    except Exception as e:
        print("⚠️ [Discovery] Erro ao buscar Google Trends:", e)
    return []

def get_mercadolivre_trends() -> list[str]:
    """
    Fetches top trending queries on Mercado Livre Brazil.
    """
    url = "https://api.mercadolibre.com/sites/MLB/trends/search"
    try:
        res = requests.get(url, timeout=10)
        if res.ok:
            data = res.json()
            return [item["keyword"].strip() for item in data if "keyword" in item]
    except Exception as e:
        print("⚠️ [Discovery] Erro ao buscar tendências do Mercado Livre:", e)
    return []

def get_next_topic(gemini_api_key: str = None) -> str | None:
    """
    Discovers the next comparison topic.
    If gemini_api_key is provided, it dynamically curates an active trend from
    Google Trends and Mercado Livre.
    Otherwise, it falls back to the static topics.json list.
    """
    data_dir = get_data_dir()
    topics_file = os.path.join(data_dir, "topics.json")
    history_file = os.path.join(data_dir, "history.json")
    
    history = []
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except Exception:
            pass

    # Dynamic AI-driven discovery
    if gemini_api_key:
        print("🔍 [Discovery] Buscando tendências ativas do Google Trends e Mercado Livre...")
        google_trends = get_google_trends()
        ml_trends = get_mercadolivre_trends()
        
        if google_trends or ml_trends:
            print(f"📊 [Discovery] Encontradas {len(google_trends)} tendências no Google e {len(ml_trends)} no Mercado Livre. Curando com IA...")
            try:
                genai.configure(api_key=gemini_api_key)
                model = genai.GenerativeModel("gemini-2.5-flash")
                
                prompt = f"""
                Você é o Diretor de Conteúdo e SEO do site "É bom?" (www.ehbom.com.br), uma vitrine inteligente de comparativos de produtos de afiliados.
                Seu objetivo é escolher a MELHOR categoria de produto físico de consumo do mercado para gerar um post de comparação hoje.
                
                Regras obrigatórias para escolha do tema:
                1. Escolha estritamente UM termo de busca curto em português que represente uma categoria de produto físico real (ex: "Fone de Ouvido Bluetooth", "Fritadeira Elétrica", "Ar Condicionado Portátil", "Cadeira Gamer", "Smartwatch").
                2. O tema DEVE ser inspirado ou ter forte correlação comercial com os tópicos quentes do Google Trends Brasil ou os termos mais buscados do Mercado Livre abaixo.
                3. Ignore celebridades, falecimentos, política, novelas, futebol, marcas específicas de vestuário, softwares, serviços ou jogos virtuais. Foque em PRODUTOS FÍSICOS DE CONSUMO (Gadgets, utilitários, eletrodomésticos, tecnologia, cosméticos).
                4. O tema NÃO deve estar na lista de comparativos já produzidos anteriormente: {json.dumps(history, ensure_ascii=False)}.
                5. Retorne APENAS um JSON no seguinte formato exato, sem blocos de código markdown adicionais:
                {{
                  "topic": "Nome do Produto Escolhido"
                }}
                
                Tópicos quentes do Google Trends Brasil de hoje:
                {json.dumps(google_trends[:20], ensure_ascii=False)}
                
                Termos buscados no Mercado Livre de hoje:
                {json.dumps(ml_trends[:20], ensure_ascii=False)}
                """
                
                response = model.generate_content(prompt)
                text = response.text.replace('```json', '').replace('```', '').strip()
                result = json.loads(text)
                topic = result.get("topic")
                if topic:
                    print(f"✨ [Discovery] Tópico viral curado por IA com sucesso: '{topic}'")
                    return topic
            except Exception as e:
                print("⚠️ [Discovery] Erro ao curar tendência com IA, usando tópicos de fallback:", e)

    # Static fallback from topics.json
    if os.path.exists(topics_file):
        try:
            with open(topics_file, 'r', encoding='utf-8') as f:
                topics = json.load(f)
            for topic in topics:
                if topic not in history:
                    print(f"📋 [Discovery] Usando tópico de fallback do topics.json: '{topic}'")
                    return topic
        except Exception as e:
            print("⚠️ [Discovery] Erro ao ler topics.json:", e)
            
    return None

def mark_topic_as_done(topic: str):
    """
    Marks a topic as processed by saving it in history.json.
    """
    data_dir = get_data_dir()
    history_file = os.path.join(data_dir, "history.json")
    
    history = []
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except Exception:
            pass
            
    if topic not in history:
        history.append(topic)
        try:
            os.makedirs(data_dir, exist_ok=True)
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("⚠️ [Discovery] Erro ao salvar histórico:", e)
