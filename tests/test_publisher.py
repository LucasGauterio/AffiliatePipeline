import os
import json
import pytest
from src.publisher import StaticPublisher

def test_static_publisher_initial_write(tmp_path):
    json_path = tmp_path / "posts.json"
    publisher = StaticPublisher(json_path=str(json_path))

    products = [
        {"title": "Prod 1", "price": "10.00", "link": "http://p1", "image_url": "http://i1", "store": "Mercado Livre"},
        {"title": "Prod 2", "price": "20.00", "link": "http://p2", "image_url": "http://i2", "store": "Mercado Livre"},
        {"title": "Prod 3", "price": "30.00", "link": "http://p3", "image_url": "http://i3", "store": "Mercado Livre"}
    ]

    post_data = {
        "title": "Melhores Fones Bluetooth de 2026",
        "content": "<p>Content description</p>"
    }

    result = publisher.publish(post_data, products)

    assert result["slug"] == "melhores-fones-bluetooth-de-2026"
    assert os.path.exists(json_path)

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        assert len(data) == 1
        post = data[0]
        assert post["slug"] == "melhores-fones-bluetooth-de-2026"
        assert post["title"] == "Melhores Fones Bluetooth de 2026"
        assert post["content"] == "<p>Content description</p>"
        assert len(post["products"]) == 3
        assert post["products"][0]["title"] == "Prod 1"
        assert post["products"][0]["badge"] == "Mais Barato"
        assert post["products"][1]["badge"] == "Custo-Benefício"
        assert post["products"][2]["badge"] == "Premium"


def test_static_publisher_append_and_update(tmp_path):
    json_path = tmp_path / "posts.json"
    publisher = StaticPublisher(json_path=str(json_path))

    products = [
        {"title": "Prod 1", "price": "10", "link": "http://p1", "store": "Amazon"},
        {"title": "Prod 2", "price": "20", "link": "http://p2", "store": "Amazon"},
        {"title": "Prod 3", "price": "30", "link": "http://p3", "store": "Amazon"}
    ]

    # 1. Publish first post
    publisher.publish({"title": "Post Um", "content": "Desc 1"}, products)
    
    # 2. Publish second post (different title -> should append)
    publisher.publish({"title": "Post Dois", "content": "Desc 2"}, products)

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        assert len(data) == 2
        assert data[0]["slug"] == "post-um"
        assert data[1]["slug"] == "post-dois"

    # 3. Publish post with same title -> should update existing entry
    updated_products = [
        {"title": "Prod 1 Updated", "price": "12", "link": "http://p1", "store": "Amazon"},
        {"title": "Prod 2", "price": "20", "link": "http://p2", "store": "Amazon"},
        {"title": "Prod 3", "price": "30", "link": "http://p3", "store": "Amazon"}
    ]
    publisher.publish({"title": "Post Um", "content": "Updated content"}, updated_products)

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        assert len(data) == 2  # No duplicates
        assert data[0]["slug"] == "post-um"
        assert data[0]["content"] == "Updated content"
        assert data[0]["products"][0]["title"] == "Prod 1_Updated" or data[0]["products"][0]["title"] == "Prod 1 Updated"


def test_static_publisher_sanitizes_content(tmp_path):
    json_path = tmp_path / "posts.json"
    publisher = StaticPublisher(json_path=str(json_path))

    products = [
        {"title": "P1", "price": "10", "link": "http://p1", "store": "Store 1"},
        {"title": "P2", "price": "20", "link": "http://p2", "store": "Store 2"},
        {"title": "P3", "price": "30", "link": "http://p3", "store": "Store 3"}
    ]

    # Injected dangerous script
    post_data = {
        "title": "Clean Post",
        "content": "<p>Content</p><script>alert('malicious');</script><strong>Clean Text</strong>"
    }

    publisher.publish(post_data, products)

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        post = data[0]
        assert "<script>" not in post["content"]
        assert "</script>" not in post["content"]
        assert "<strong>Clean Text</strong>" in post["content"]
