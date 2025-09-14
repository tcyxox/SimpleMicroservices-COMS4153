from __future__ import annotations

import os

from pydantic import StringConstraints
from fastapi import FastAPI, HTTPException, Query, status
from typing import Dict, List, Optional, Annotated
from datetime import datetime

from models.course import CourseCreate, CourseRead, CourseUpdate
from models.professor import ProfessorCreate, ProfessorRead, ProfessorUpdate

port = int(os.environ.get("FASTAPIPORT", 8000))

app = FastAPI(
    title="Professor/Course API",
    description="Demo FastAPI app using Pydantic v2 models for Person and Address",
    version="0.1.0",
)

idType = Annotated[str, StringConstraints(pattern=r"^[a-z]{2,3}\d{1,4}$")]
courseIDType = Annotated[str, StringConstraints(pattern=r"^[A-Z]{4}\d{4}$")]

# simple in-memory databases
professors: Dict[idType, ProfessorRead] = {}
courses: Dict[courseIDType, CourseRead] = {}


# -----------------------------------------------------------------------------
# Professor endpoints
# -----------------------------------------------------------------------------
@app.post("/professors", response_model=ProfessorRead, status_code=201, tags=["Professors"])
def create_professor(professor: ProfessorCreate):
    """
    Create a new professor record.
    The professor's Columbia ID (`id`) is unique.
    """
    # Check if the Columbia ID already exists to prevent duplicates
    if any(p.id == professor.id for p in professors.values()):
        raise HTTPException(
            status_code=400,
            detail=f"Professor with Columbia ID '{professor.id}' already exists.",
        )
    new_professor = ProfessorRead(**professor.model_dump())
    professors[new_professor.id] = new_professor
    return new_professor


@app.get("/professors", response_model=List[ProfessorRead], tags=["Professors"])
def list_professors(
        first_name: Optional[str] = Query(None, description="Filter by first name"),
        last_name: Optional[str] = Query(None, description="Filter by last name"),
        id: Optional[str] = Query(None, description="Filter by Columbia ID"),
):
    """Get a list of all professors, with optional filtering."""
    results = list(professors.values())

    if first_name:
        results = [p for p in results if p.first_name.lower() == first_name.lower()]
    if last_name:
        results = [p for p in results if p.last_name.lower() == last_name.lower()]
    if id:
        results = [p for p in results if p.id == id]

    return results


@app.get("/professors/{professor_id}", response_model=ProfessorRead, tags=["Professors"])
def get_professor(professor_id: idType):
    """Get a single professor by their id."""
    if professor_id not in professors:
        raise HTTPException(status_code=404, detail="Professor not found")
    return professors[professor_id]


@app.patch("/professors/{professor_id}", response_model=ProfessorRead, tags=["Professors"])
def update_professor(professor_id: idType, update_data: ProfessorUpdate):
    """Partially update a professor's information."""
    if professor_id not in professors:
        raise HTTPException(status_code=404, detail="Professor not found")

    stored_professor_data = professors[professor_id].model_dump()
    update_dict = update_data.model_dump(exclude_unset=True)

    stored_professor_data.update(update_dict)
    # Manually update the `updated_at` timestamp
    stored_professor_data["updated_at"] = datetime.utcnow()

    updated_professor = ProfessorRead(**stored_professor_data)
    professors[professor_id] = updated_professor
    return updated_professor


@app.delete("/professors/{professor_id}", status_code=204, tags=["Professors"])
def delete_professor(professor_id: idType):
    """Delete a professor."""
    if professor_id not in professors.keys():
        raise HTTPException(status_code=404, detail=f"Professor with ID {professor_id} not found")
    del professors[professor_id]


# -----------------------------------------------------------------------------
# Course endpoints
# -----------------------------------------------------------------------------
@app.post("/courses", response_model=CourseRead, status_code=201, tags=["Courses"])
def create_course(course: CourseCreate):
    """
    Create a new course record.
    The course ID (`courseID`) must be unique.
    """
    if any(c.courseID == course.courseID for c in courses.values()):
        raise HTTPException(
            status_code=400,
            detail=f"Course with ID '{course.courseID}' already exists.",
        )

    new_course = CourseRead(**course.model_dump())
    courses[new_course.courseID] = new_course
    return new_course


@app.get("/courses", response_model=List[CourseRead], tags=["Courses"])
def list_courses(
        course_id: Optional[courseIDType] = Query(None, description="Filter by course id"),
        course_name: Optional[str] = Query(None, description="Filter by course name"),
        instructor_id: Optional[str] = Query(None, description="Filter by instructor's Columbia ID"),
):
    """Get a list of all courses, with optional filtering."""
    results = list(courses.values())

    if course_id:
        results = [c for c in results if c.courseID and c.courseID == course_id]
    if course_name:
        results = [c for c in results if course_name.lower() in c.courseName.lower()]
    if instructor_id:
        results = [c for c in results if c.instructor and c.instructor.id == instructor_id]

    return results


@app.get("/courses/{course_id}", response_model=CourseRead, tags=["Courses"])
def get_course(course_id: courseIDType):
    """Get a single course by its course_id."""
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    return courses[course_id]


@app.patch("/courses/{course_id}", response_model=CourseRead, tags=["Courses"])
def update_course(course_id: courseIDType, update_data: CourseUpdate):
    """Partially update a course's information."""
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")

    stored_course_data = courses[course_id].model_dump()
    update_dict = update_data.model_dump(exclude_unset=True)

    stored_course_data.update(update_dict)
    stored_course_data["updated_at"] = datetime.utcnow()

    updated_course = CourseRead(**stored_course_data)
    courses[course_id] = updated_course
    return updated_course


@app.delete("/courses/{course_id}", status_code=204, tags=["Courses"])
def delete_course(course_id: courseIDType):
    """Delete a course."""
    if course_id not in courses:
        raise HTTPException(status_code=404, detail=f"Course with ID {course_id} not found")
    print(len(courses))
    del courses[course_id]


# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Professor/Course API. See /docs for OpenAPI UI."}


# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True)
