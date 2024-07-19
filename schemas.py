from pydantic import BaseModel
from typing import Optional


class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = None


class StudentCreate(BaseModel):
    name: str
    email: str
    age: Optional[int] = None


class CourseResponse(CourseCreate):
    id: int

    class Config:
        orm_mode = True


class StudentResponse(StudentCreate):
    id: int

    class Config:
        orm_mode = True
