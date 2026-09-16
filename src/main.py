from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Student Management API")


# Student model
class Student(BaseModel):
    id: int
    name: str
    department: str
    semester: int
    cgpa: float


# Temporary student data
students = [
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
]


# ---------------- GET ----------------

# Get all students
@app.get("/students")
def get_students():
    return students


# Get a student by ID
@app.get("/students/{student_id}")
def get_student(student_id: int):

    for student in students:
        if student.id == student_id:
            return student

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )


# ---------------- POST ----------------

# Add a new student
@app.post("/students", status_code=201)
def create_student(student: Student):

    # Check duplicate ID
    for existing_student in students:
        if existing_student.id == student.id:
            raise HTTPException(
                status_code=400,
                detail="Student ID already exists"
            )

    students.append(student)

    return {
        "message": "Student created successfully",
        "student": student
    }


# ---------------- PUT ----------------

# Update an existing student
@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):

    for index, student in enumerate(students):

        if student.id == student_id:

            # Make sure URL ID and body ID match
            if updated_student.id != student_id:
                raise HTTPException(
                    status_code=400,
                    detail="Student ID in URL and body must match"
                )

            students[index] = updated_student

            return {
                "message": "Student updated successfully",
                "student": updated_student
            }

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )


# ---------------- DELETE ----------------

# Delete a student
@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    for index, student in enumerate(students):

        if student.id == student_id:

            deleted_student = students.pop(index)

            return {
                "message": "Student deleted successfully",
                "student": deleted_student
            }

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )