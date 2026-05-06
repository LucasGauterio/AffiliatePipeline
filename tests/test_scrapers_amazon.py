import pytest
from src.scrapers.amazon import AmazonScraper

def test_amazon_scraper_parsing(mocker):
    # Simulated Amazon HTML search results page
    mock_html = """
    <html>
    <body>
        <div data-component-type="s-search-result">
            <h2>
                <a href="/dp/B08MKBMMWW">
                    <span>Logitech Pebble Mouse Sem Fio</span>
                </a>
            </h2>
            <img class="s-image" src="https://images.amazon.com/mouse.jpg" />
            <span class="a-price"><span class="a-offscreen">R$ 120,50</span></span>
        </div>
        <div data-component-type="s-search-result">
            <h2>
                <a href="/dp/B08MKBMXYZ">
                    <span>Mouse Multilaser Sem Fio Básico</span>
                </a>
            </h2>
            <img class="s-image" src="https://images.amazon.com/basic.jpg" />
            <span class="a-price"><span class="a-offscreen">R$ 35,90</span></span>
        </div>
        <div data-component-type="s-search-result">
            <h2>
                <a href="/dp/B08MKBMABC">
                    <span>Razer DeathAdder Pro V3 Premium</span>
                </a>
            </h2>
            <img class="s-image" src="https://images.amazon.com/razer.jpg" />
            <span class="a-price"><span class="a-offscreen">R$ 899,00</span></span>
        </div>
    </body>
    </html>
    """
    
    mock_response = mocker.Mock()
    mock_response.ok = True
    mock_response.status_code = 200
    mock_response.text = mock_html
    
    mocker.patch('requests.get', return_value=mock_response)
    
    scraper = AmazonScraper()
    results = scraper.scrape("Mouse sem Fio")
    
    assert isinstance(results, list)
    assert len(results) == 3
    
    # Verify price-sorting and badges:
    # 1. Mais Barato (R$ 35.90)
    assert results[0]["badge"] == "Mais Barato"
    assert results[0]["title"] == "Mouse Multilaser Sem Fio Básico"
    assert results[0]["price"] == "35.90"
    assert results[0]["link"] == "https://www.amazon.com.br/dp/B08MKBMXYZ"
    assert results[0]["image_url"] == "https://images.amazon.com/basic.jpg"
    assert results[0]["store"] == "Amazon"
    
    # 2. Custo-Benefício (R$ 120.50)
    assert results[1]["badge"] == "Custo-Benefício"
    assert results[1]["title"] == "Logitech Pebble Mouse Sem Fio"
    assert results[1]["price"] == "120.50"
    assert results[1]["link"] == "https://www.amazon.com.br/dp/B08MKBMMWW"
    
    # 3. Premium (R$ 899.00)
    assert results[2]["badge"] == "Premium"
    assert results[2]["title"] == "Razer DeathAdder Pro V3 Premium"
    assert results[2]["price"] == "899.00"
