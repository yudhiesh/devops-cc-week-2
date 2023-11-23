def test_health_route(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert b'healthy' == response.data


def test_quote_route(client):
    response = client.get('/quote')
    assert response.data is not None