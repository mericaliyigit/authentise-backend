from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_create_pet():
    response = client.post(
        "/pets/",
        headers={"X-Token": "coneofsilence"},
        json={
            "name": "Milo",
            "breed": "Jack Russell Terrier",
            "rank": 50,
            "type": "dog",
            "img_url": "https://www.google.com"
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        "detail": "Successfully created pet with name Milo"
    }

    response = client.post(
        "/pets/",
        headers={"X-Token": "coneofsilence"},
        json={
            "name": "Kitmir",
            "breed": "Anatolian Shepherd",
            "rank": 100,
            "type": "dog",
            "img_url": "https://www.google.com"
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        "detail": "Successfully created pet with name Kitmir"
    }


def test_get_pet():
    response = client.get("/pets/Milo", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {'name': 'Milo', 'breed': 'Jack Russell Terrier', 'rank': 50,
                               'type': 'dog', 'img_url': 'https://www.google.com'}

    response = client.get(
        "/pets/?type=dog", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "Kitmir",
            "breed": "Anatolian Shepherd",
            "rank": 100,
            "type": "dog",
            "img_url": "https://www.google.com"
        },
        {
            'name': 'Milo',
            'breed': 'Jack Russell Terrier',
            'rank': 50,
            'type': 'dog',
            'img_url': 'https://www.google.com'
        }
    ]

    response = client.get("/pets/Masha", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {'detail': 'There is no pet with name Masha'}


def test_delete_pet():
    response = client.delete(
        "/pets/Milo",
        headers={"X-Token": "coneofsilence"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "detail": "Successfully deleted pet with name Milo"
    }

    response = client.delete(
        "/pets/?type=dog",
        headers={"X-Token": "coneofsilence"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "detail": "Successfully deleted 1 pets with type dog"
    }
