from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import sessionmaker
from database import SessionLocal, engine, Base
from models import Course, Student  # Import your SQLAlchemy models here
from schemas import CourseCreate, StudentCreate, CourseResponse, StudentResponse  # Import from schemas.py
from typing import List, Optional

# Initialize FastAPI app
app = FastAPI()


# Create the database tables if not already created
# Ensure to use this cautiously, as it will not run migrations. Migrations should be handled by Alembic.
# Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CRUD operations and endpoints

@app.post("/courses/", response_model=CourseResponse)
def create_course(course: CourseCreate, db: sessionmaker = Depends(get_db)):
    db_course = Course(title=course.title, description=course.description)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


@app.get("/courses/", response_model=List[CourseResponse])
def read_courses(skip: int = 0, limit: int = 10, db: sessionmaker = Depends(get_db)):
    courses = db.query(Course).offset(skip).limit(limit).all()
    return courses


@app.get("/courses/{course_id}", response_model=CourseResponse)
def read_course(course_id: int, db: sessionmaker = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@app.put("/courses/{course_id}", response_model=CourseResponse)
def update_course(course_id: int, course: CourseCreate, db: sessionmaker = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    db_course.title = course.title
    db_course.description = course.description
    db.commit()
    db.refresh(db_course)
    return db_course


@app.post("/students/", response_model=StudentResponse)
def create_student(student: StudentCreate, db: sessionmaker = Depends(get_db)):
    db_student = Student(name=student.name, email=student.email, age=student.age)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@app.get("/students/", response_model=List[StudentResponse])
def read_students(skip: int = 0, limit: int = 10, db: sessionmaker = Depends(get_db)):
    students = db.query(Student).offset(skip).limit(limit).all()
    return students


@app.get("/students/{student_id}", response_model=StudentResponse)
def read_student(student_id: int, db: sessionmaker = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student: StudentCreate, db: sessionmaker = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    db_student.name = student.name
    db_student.email = student.email
    db_student.age = student.age
    db.commit()
    db.refresh(db_student)
    return db_student
