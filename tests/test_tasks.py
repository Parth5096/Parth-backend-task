from http import HTTPStatus


def get_token(client, email="u@e.com", password="secret123", role=None):
    payload = {"email": email, "password": password}
    if role:
        payload["role"] = role
    client.post("/auth/register", json=payload)
    token = client.post("/auth/login", json={"email": email, "password": password}).get_json()["access_token"]
    return token


def auth_headers(client, email="u@e.com", password="secret123", role=None):
    token = get_token(client, email=email, password=password, role=role)
    return {"Authorization": f"Bearer {token}"}


def test_crud_flow(client):
    headers = auth_headers(client)

    # create
    res = client.post("/tasks", json={"title": "T1", "description": "d"}, headers=headers)
    assert res.status_code == HTTPStatus.CREATED
    tid = res.get_json()["id"]

    # list
    res = client.get("/tasks", headers=headers)
    assert res.status_code == HTTPStatus.OK
    assert res.get_json()["total"] == 1

    # get
    res = client.get(f"/tasks/{tid}", headers=headers)
    assert res.status_code == HTTPStatus.OK

    # update
    res = client.put(f"/tasks/{tid}", json={"completed": True}, headers=headers)
    assert res.status_code == HTTPStatus.OK
    assert res.get_json()["completed"] is True

    # delete
    res = client.delete(f"/tasks/{tid}", headers=headers)
    assert res.status_code == HTTPStatus.NO_CONTENT


def test_pagination_and_filtering(client):
    headers = auth_headers(client)
    for i in range(25):
        client.post("/tasks", json={"title": f"T{i}", "completed": i % 2 == 0}, headers=headers)

    res = client.get("/tasks?per_page=5&page=2&completed=true", headers=headers)
    data = res.get_json()
    assert res.status_code == HTTPStatus.OK
    assert data["page"] == 2
    assert data["per_page"] == 5
    assert all(item["completed"] for item in data["items"])  

    # completed=false
    res = client.get("/tasks?completed=false", headers=headers)
    data = res.get_json()
    assert res.status_code == HTTPStatus.OK
    assert all(not item["completed"] for item in data["items"])


def test_validation_errors_and_404(client):
    headers = auth_headers(client)

    res = client.post("/tasks", json={"description": "no title"}, headers=headers)
    assert res.status_code == HTTPStatus.BAD_REQUEST

    # non-existent -> 404
    res = client.get("/tasks/9999", headers=headers)
    assert res.status_code == HTTPStatus.NOT_FOUND


def test_ownership_enforced_for_non_admin(client):
    # user A creates
    headers_a = auth_headers(client, email="a1@ex.com")
    t = client.post("/tasks", json={"title": "A's Task"}, headers=headers_a).get_json()

    # user B tries to access A's task
    headers_b = auth_headers(client, email="b1@ex.com")
    res = client.get(f"/tasks/{t['id']}", headers=headers_b)
    assert res.status_code == HTTPStatus.FORBIDDEN

    res = client.put(f"/tasks/{t['id']}", json={"completed": True}, headers=headers_b)
    assert res.status_code == HTTPStatus.FORBIDDEN

    res = client.delete(f"/tasks/{t['id']}", headers=headers_b)
    assert res.status_code == HTTPStatus.FORBIDDEN


def test_admin_can_access_any_task(client):
    # normal user creates a task
    headers_user = auth_headers(client, email="user1@ex.com")
    t = client.post("/tasks", json={"title": "U Task"}, headers=headers_user).get_json()

    # admin can read/update/delete it
    headers_admin = auth_headers(client, email="admin@ex.com", role="admin")

    r = client.get(f"/tasks/{t['id']}", headers=headers_admin)
    assert r.status_code == HTTPStatus.OK

    r = client.put(f"/tasks/{t['id']}", json={"completed": True}, headers=headers_admin)
    assert r.status_code == HTTPStatus.OK
    assert r.get_json()["completed"] is True

    r = client.delete(f"/tasks/{t['id']}", headers=headers_admin)
    assert r.status_code == HTTPStatus.NO_CONTENT


def test_list_without_token_returns_empty(client):
    # optional auth: no token -> empty list
    res = client.get("/tasks")
    assert res.status_code == HTTPStatus.OK
    payload = res.get_json()
    assert payload["items"] == []
    assert payload["total"] == 0
