import pytest
from unittest.mock import patch, MagicMock
from src.publisher import WordPressPublisher

@patch("src.publisher.requests.post")
def test_publisher_create_payload_and_post(mock_post):
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"id": 123}
    mock_post.return_value = mock_response

    publisher = WordPressPublisher(
        wp_url="https://example.com",
        wp_user="admin",
        wp_password="password"
    )

    products = [
        {"title": "Prod 1", "price": "10", "link": "http://p1", "store": "Store 1"},
        {"title": "Prod 2", "price": "20", "link": "http://p2", "store": "Store 2"},
        {"title": "Prod 3", "price": "30", "link": "http://p3", "store": "Store 3"}
    ]

    # Malicious script injected by AI
    post_data = {
        "title": "My Post",
        "content": "<p>Content</p><script>alert('xss');</script>"
    }

    result = publisher.publish(post_data, products)

    assert result == {"id": 123}
    mock_post.assert_called_once()
    
    args, kwargs = mock_post.call_args
    assert kwargs["auth"] == ("admin", "password")
    
    payload = kwargs["json"]
    assert payload["title"] == "My Post"
    assert payload["status"] == "publish"
    
    # Check Bleach sanitization
    assert "<script>" not in payload["content"]
    assert "&lt;script&gt;" in payload["content"] or "alert" not in payload["content"] or "<p>Content</p>" in payload["content"]

    # Check ACF payload
    acf = payload["acf"]
    assert acf["product_1_title"] == "Prod 1"
    assert acf["product_2_price"] == "20"
    assert acf["product_3_store"] == "Store 3"
