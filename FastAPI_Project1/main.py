from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "API is running"
    }


students = [
    {
        "id": 1,
        "name": "Abhishek",
        "course": "AIML"
    },

    {
        "id": 2,
        "name": "Rohit",
        "course": "Data Science"
    }
]

@app.get("/students")
def get_students():
    return students

@app.get("/students/{student_id}")
def get_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student
    return {"message": "Student not found"}

@app.get("/students/{student_id}")

def get_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student

    return {"message": "Student not found"}


from pydantic import BaseModel

class Student(BaseModel):
    id: int
    name: str
    course : str

@app.post("/students")

def add_student(student: Student):
    students.append(student.dict())
    return {
        "message": "Student added successfully",
        "student": student
    }

@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):

    for student in students:
        if student["id"] == student_id:
            student["name"] = updated_student.name
            student["course"] = updated_student.course
            return {
                "message": "Student updated successfully",
                "student": student
            }
    return {"message": "Student not found"}


@app.delete("/students/{student_id}")

def delete_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            return {"message": "Student deleted successfully"}
    return {"message": "Student not found"}