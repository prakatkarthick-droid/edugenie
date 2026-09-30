from fastapi.testclient import TestClient
import main
import ai_client

client = TestClient(main.app)

def test_homepage_loads():
    response = client.get('/')
    assert response.status_code == 200
    assert 'EduGenie' in response.text

def test_health_endpoint():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'

def test_empty_text_is_rejected():
    response = client.post('/qa', json={'text': ''})
    assert response.status_code == 422

def test_explain_without_key_has_fallback(monkeypatch):
    monkeypatch.delenv('GEMINI_API_KEY', raising=False)
    monkeypatch.setenv('ENABLE_LOCAL_EXPLAINER', 'false')
    ai_client._client.cache_clear()
    response = client.post('/explain', json={'text': 'photosynthesis'})
    assert response.status_code == 200
    assert 'photosynthesis' in response.json()['result']
