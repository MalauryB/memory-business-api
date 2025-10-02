import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from main import app


@pytest.fixture(scope="session")
def event_loop():
    """Crée une event loop pour toute la session de tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def client():
    """Crée un client HTTP de test."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_health_endpoint(client):
    """Test de l'endpoint de santé."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_root_endpoint(client):
    """Test de l'endpoint racine."""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["docs"] == "/docs"


@pytest.mark.asyncio
async def test_create_and_get_client(client):
    """Test E2E: créer un client puis le récupérer."""
    # Créer un client
    client_data = {
        "name": "Test Corp",
        "contact_name": "John Doe",
        "email": "john@testcorp.com",
        "phone": "+33 1 23 45 67 89",
        "address": {
            "street": "123 Test St",
            "city": "Paris",
            "zip_code": "75001",
            "country": "France"
        }
    }

    create_response = await client.post("/api/clients/", json=client_data)
    assert create_response.status_code == 201
    created_client = create_response.json()

    assert created_client["name"] == client_data["name"]
    assert created_client["email"] == client_data["email"]
    assert "id" in created_client
    client_id = created_client["id"]

    # Récupérer le client créé
    get_response = await client.get(f"/api/clients/{client_id}")
    assert get_response.status_code == 200
    retrieved_client = get_response.json()

    assert retrieved_client["id"] == client_id
    assert retrieved_client["name"] == client_data["name"]


@pytest.mark.asyncio
async def test_list_clients(client):
    """Test E2E: lister les clients."""
    response = await client.get("/api/clients/")
    assert response.status_code == 200
    clients = response.json()
    assert isinstance(clients, list)


@pytest.mark.asyncio
async def test_update_client(client):
    """Test E2E: créer un client, le mettre à jour."""
    # Créer un client
    client_data = {
        "name": "Update Test Corp",
        "contact_name": "Jane Doe",
        "email": "jane@updatetest.com",
        "phone": "+33 1 11 22 33 44",
        "address": {
            "street": "456 Update St",
            "city": "Lyon",
            "zip_code": "69001",
            "country": "France"
        }
    }

    create_response = await client.post("/api/clients/", json=client_data)
    assert create_response.status_code == 201
    client_id = create_response.json()["id"]

    # Mettre à jour le client
    update_data = {
        "name": "Updated Corp Name",
        "email": "newemail@updatetest.com"
    }

    update_response = await client.put(f"/api/clients/{client_id}", json=update_data)
    assert update_response.status_code == 200
    updated_client = update_response.json()

    assert updated_client["name"] == update_data["name"]
    assert updated_client["email"] == update_data["email"]
    assert updated_client["contact_name"] == client_data["contact_name"]  # Inchangé


@pytest.mark.asyncio
async def test_delete_client(client):
    """Test E2E: créer un client puis le supprimer."""
    # Créer un client
    client_data = {
        "name": "Delete Test Corp",
        "contact_name": "Delete User",
        "email": "delete@test.com",
        "phone": "+33 1 99 88 77 66",
        "address": {
            "street": "789 Delete St",
            "city": "Marseille",
            "zip_code": "13001",
            "country": "France"
        }
    }

    create_response = await client.post("/api/clients/", json=client_data)
    assert create_response.status_code == 201
    client_id = create_response.json()["id"]

    # Supprimer le client
    delete_response = await client.delete(f"/api/clients/{client_id}")
    assert delete_response.status_code == 204

    # Vérifier que le client n'existe plus
    get_response = await client.get(f"/api/clients/{client_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_graphql_hello(client):
    """Test E2E: query GraphQL simple."""
    query = """
    query {
        hello
    }
    """

    response = await client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert data["data"]["hello"] == "Hello from GraphQL!"
