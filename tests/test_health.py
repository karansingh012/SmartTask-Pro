from app import create_app


def test_health_check():
    app = create_app("config.TestingConfig")
    client = app.test_client()

    response = client.get("/tasks/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
