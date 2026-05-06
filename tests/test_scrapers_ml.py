import pytest
from src.scrapers.mercadolivre import MercadoLivreScraper

def test_mercadolivre_scraper_parsing(mocker):
    # Simulated Mercado Livre public JSON search results API
    mock_api_response = {
        "results": [
            {
                "title": "Fone de Ouvido Bluetooth Anker Soundcore Q30",
                "price": 349.90,
                "permalink": "https://produto.mercadolivre.com.br/soundcore-q30",
                "secure_thumbnail": "https://http2.mlstatic.com/D_NQ_NP_987654-MLB-I.jpg"
            },
            {
                "title": "Borracha Protetora de Silicone para Fone",
                "price": 5.90,  # Below R$ 15.00, should be filtered out as accessory noise!
                "permalink": "https://produto.mercadolivre.com.br/borracha-silicone",
                "secure_thumbnail": "https://http2.mlstatic.com/D_NQ_NP_123456-MLB-I.jpg"
            },
            {
                "title": "Fone de Ouvido Bluetooth Kaidi KD-771 Básico",
                "price": 59.90,
                "permalink": "https://produto.mercadolivre.com.br/kaidi-kd771",
                "secure_thumbnail": "https://http2.mlstatic.com/D_NQ_NP_112233-MLB-V.jpg"
            },
            {
                "title": "Fone de Ouvido Noise Cancelling Sony WH-1000XM5",
                "price": 1999.00,
                "permalink": "https://produto.mercadolivre.com.br/sony-xm5",
                "secure_thumbnail": "https://http2.mlstatic.com/D_NQ_NP_445566-MLB-O.jpg"
            }
        ]
    }
    
    mock_response = mocker.Mock()
    mock_response.ok = True
    mock_response.status_code = 200
    mock_response.json = lambda: mock_api_response
    
    mocker.patch('requests.get', return_value=mock_response)
    
    scraper = MercadoLivreScraper()
    results = scraper.scrape("Fone de Ouvido")
    
    assert isinstance(results, list)
    assert len(results) == 3  # The accessory (R$ 5.90) should be discarded, leaving 3 items
    
    # Verify sorting and HD image upgrade:
    # 1. Mais Barato (R$ 59.90 Kaidi)
    assert results[0]["badge"] == "Mais Barato"
    assert results[0]["title"] == "Fone de Ouvido Bluetooth Kaidi KD-771 Básico"
    assert results[0]["price"] == "59.90"
    assert results[0]["link"] == "https://produto.mercadolivre.com.br/kaidi-kd771"
    assert results[0]["image_url"] == "https://http2.mlstatic.com/D_NQ_NP_112233-MLB-O.jpg"  # Upgraded to HD (-O.jpg)!
    assert results[0]["store"] == "Mercado Livre"
    
    # 2. Custo-Benefício (R$ 349.90 Anker)
    assert results[1]["badge"] == "Custo-Benefício"
    assert results[1]["title"] == "Fone de Ouvido Bluetooth Anker Soundcore Q30"
    assert results[1]["price"] == "349.90"
    assert results[1]["image_url"] == "https://http2.mlstatic.com/D_NQ_NP_987654-MLB-O.jpg"  # Upgraded to HD (-O.jpg)!
    
    # 3. Premium (R$ 1999.00 Sony)
    assert results[2]["badge"] == "Premium"
    assert results[2]["title"] == "Fone de Ouvido Noise Cancelling Sony WH-1000XM5"
    assert results[2]["price"] == "1999.00"
    assert results[2]["image_url"] == "https://http2.mlstatic.com/D_NQ_NP_445566-MLB-O.jpg"
