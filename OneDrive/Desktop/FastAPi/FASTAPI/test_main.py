from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# test home api
def test_home():
    response = client.get("/")
    assert response.status_code == 200 #status code check
    assert response.json() == {"message": "Welcome to the FastAPI application!"}#response data check

# test add api
def test_add():
    response = client.get("/add?a=5&b=3")
    assert response.status_code == 200 #status code check
    assert response.json() == {"result": 8} #response data check