from http import HTTPStatus


def test_register_and_login(client):
    # register
    res = client.post("/auth/register", json={"email": "a@b.com", "password": "secret123"})
    assert res.status_code == HTTPStatus.CREATED

    # login
    res = client.post("/auth/login", json={"email": "a@b.com", "password": "secret123"})
    assert res.status_code == HTTPStatus.OK
    assert "access_token" in res.get_json()


def test_register_duplicate_email(client):
    client.post("/auth/register", json={"email": "dup@e.com", "password": "secret123"})
    res = client.post("/auth/register", json={"email": "dup@e.com", "password": "secret123"})
    assert res.status_code == HTTPStatus.BAD_REQUEST


def test_login_wrong_password(client):
    client.post("/auth/register", json={"email": "x@y.com", "password": "secret123"})
    res = client.post("/auth/login", json={"email": "x@y.com", "password": "bad"})
    assert res.status_code == HTTPStatus.UNAUTHORIZED


def test_protected_requires_token(client):
    res = client.get("/tasks/1")
    assert res.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.NOT_FOUND)
