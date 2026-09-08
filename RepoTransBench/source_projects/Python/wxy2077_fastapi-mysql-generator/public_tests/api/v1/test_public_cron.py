from fastapi.testclient import TestClient

def test_add_job_public(client: TestClient, superuser_token_headers: dict) -> None:
    public_job_id = "public_job_786"
    response = client.post("/job/schedule", json={
        "seconds": 8,
        "job_id": public_job_id
    }, headers=superuser_token_headers)
    assert response.status_code == 200
    assert response.json()["code"] == 200
    assert response.json()["data"]["id"] == public_job_id

def test_get_all_job_public(client: TestClient, superuser_token_headers: dict) -> None:
    response = client.get("/jobs/all", headers=superuser_token_headers)
    assert response.status_code == 200
    assert response.json()["code"] == 200
    assert isinstance(response.json()["data"], list)

def test_del_job_public(client: TestClient, superuser_token_headers: dict) -> None:
    # Use a public job id for this test
    public_job_id = "public_job_786"
    response = client.post("/job/del", json={
        "job_id": public_job_id
    }, headers=superuser_token_headers)
    assert response.status_code == 200
    assert response.json()["code"] == 200