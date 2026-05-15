import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_users_crud_flow(client: AsyncClient):
    """Prueba el ciclo de vida completo de un usuario en un solo flujo."""
    payload = {
        "username": "luioscaTest",
        "email": "luiosca@gmail.com",
        "first_name": "Luis Esteban",
        "last_name": "Osorio Castaneda",
        "role": "user",
        "active": True,
    }

    # 1. Crear
    create_response = await client.post("/users/", json=payload)
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["email"] == payload["email"]
    assert "id" in created

    user_id = created["id"]

    # 2. Consultar
    get_response = await client.get(f"/users/{user_id}")
    assert get_response.status_code == 200
    fetched = get_response.json()
    assert fetched["id"] == user_id

    # 3. Actualizar
    update_response = await client.put(
        f"/users/{user_id}", json={"first_name": "Jane", "role": "admin"}
    )
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["first_name"] == "Jane"
    assert updated["role"] == "admin"

    # 4. Listar
    list_response = await client.get("/users/")
    assert list_response.status_code == 200
    assert any(user["id"] == user_id for user in list_response.json())

    # 5. Borrar (Ajustado a 200 según la configuración de tu router)
    delete_response = await client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 200

    # 6. Verificar que ya no existe
    missing_response = await client.get(f"/users/{user_id}")
    assert missing_response.status_code == 404


@pytest.mark.asyncio
async def test_duplicate_user_validation(client: AsyncClient):
    """Prueba que el sistema rechace correos o usuarios duplicados (Camino triste)."""
    payload = {
        "username": "jennymartinezTest",
        "email": "jennymartinez@gmail.com",
        "first_name": "Jenny",
        "last_name": "Martinez",
        "role": "user",
        "active": True,
    }

    # Lo creamos la primera vez con éxito
    await client.post("/users/", json=payload)

    # Intentamos crearlo de nuevo, debería lanzar error 400
    duplicate_response = await client.post("/users/", json=payload)
    assert duplicate_response.status_code == 400
    assert "already registered" in duplicate_response.json()["detail"].lower()