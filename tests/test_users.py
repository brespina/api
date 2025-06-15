from app import schemas

def test_create_user(client):
    payload = {"email": "ana@uh.edu", "first_name": "Ana", "last_name": "Ng"}
    r = client.post("/users/", json=payload)
    assert r.status_code == 201
    data = schemas.UserRead(**r.json())      # validate payload with Pydantic
    assert data.email == payload["email"]

def test_duplicate_email(client):
    p = {"email": "dupe@uh.edu"}
    client.post("/users/", json=p)
    r = client.post("/users/", json=p)
    assert r.status_code == 400
    assert r.json()["detail"] == "Email already registered"

def test_list_users(client):
    client.post("/users/", json={"email": "one@uh.edu"})
    client.post("/users/", json={"email": "two@uh.edu"})
    r = client.get("/users/")
    assert r.status_code == 200
    assert len(r.json()) >= 2
