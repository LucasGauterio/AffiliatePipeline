import os
import json

def get_data_dir():
    return os.getenv("DATA_DIR", os.path.join(os.path.dirname(__file__), "..", "data"))

def get_next_topic() -> str | None:
    data_dir = get_data_dir()
    topics_file = os.path.join(data_dir, "topics.json")
    history_file = os.path.join(data_dir, "history.json")
    
    if not os.path.exists(topics_file):
        raise FileNotFoundError(f"Topics file not found at {topics_file}")
        
    with open(topics_file, 'r', encoding='utf-8') as f:
        topics = json.load(f)
        
    history = []
    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)
            
    for topic in topics:
        if topic not in history:
            return topic
            
    return None

def mark_topic_as_done(topic: str):
    data_dir = get_data_dir()
    history_file = os.path.join(data_dir, "history.json")
    
    history = []
    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)
            
    if topic not in history:
        history.append(topic)
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
