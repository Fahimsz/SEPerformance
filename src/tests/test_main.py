import pytest
from fastapi.testclient import TestClient

from src.main import app, students, Student

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_students():
    students.clear()

    students.extend([
        Student(
            id=1,
            name="Fahim",
            department="CSE",
            semester=5,
            cgpa=3.75
        ),
        Student(
            id=2,
            name="Rahim",
            department="EEE",
            semester=4,
            cgpa=3.50
        )
    ])


# ================= GET =================

def test_get_all_students():
    response = client.get("/students")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_student_by_id():
    response = client.get("/students/1")

    assert response.status_code == 200
    assert response.json()["name"] == "Fahim"


def test_get_nonexistent_student():
    response = client.get("/students/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"


# ================= POST =================

def test_create_student():
    student = {
        "id": 3,
        "name": "Karim",
        "department": "CSE",
        "semester": 6,
        "cgpa": 3.82
    }

    response = client.post("/students", json=student)

    assert response.status_code == 201
    assert response.json()["message"] == "Student created successfully"


def test_create_duplicate_student():
    student = {
        "id": 1,
        "name": "Another Student",
        "department": "CSE",
        "semester": 3,
        "cgpa": 3.20
    }

    response = client.post("/students", json=student)

    assert response.status_code == 400
    assert response.json()["detail"] == "Student ID already exists"


# ================= PUT =================

def test_update_student():
    student = {
        "id": 1,
        "name": "Fahim Updated",
        "department": "CSE",
        "semester": 6,
        "cgpa": 3.90
    }

    response = client.put("/students/1", json=student)

    assert response.status_code == 200
    assert response.json()["student"]["name"] == "Fahim Updated"


def test_update_nonexistent_student():
    student = {
        "id": 999,
        "name": "Unknown",
        "department": "CSE",
        "semester": 5,
        "cgpa": 3.50
    }

    response = client.put("/students/999", json=student)

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"


def test_update_with_mismatched_id():
    student = {
        "id": 2,
        "name": "Fahim",
        "department": "CSE",
        "semester": 5,
        "cgpa": 3.80
    }

    response = client.put("/students/1", json=student)

    assert response.status_code == 400


# ================= DELETE =================

def test_delete_student():
    response = client.delete("/students/1")

    assert response.status_code == 200
    assert response.json()["student"]["id"] == 1


def test_delete_nonexistent_student():
    response = client.delete("/students/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"