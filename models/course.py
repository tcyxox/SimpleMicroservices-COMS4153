from __future__ import annotations
from pydantic import Field, BaseModel, StringConstraints
from typing import Annotated, List, Optional
from uuid import UUID, uuid4
from datetime import date, datetime
from .professor import ProfessorBase

courseIDType = Annotated[str, StringConstraints(pattern=r"^[A-Z]{4}\d{4}$")]


class CourseBase(BaseModel):
    courseID: courseIDType = Field(
        ...,
        description="The ID of a course (4 capital letters + 4 digits).",
        json_schema_extra={"example": "COMS4153"},
    )
    courseName: str = Field(
        ...,
        description="The name of the course.",
        json_schema_extra={"example": "Cloud Computing"},
    )
    instructor: ProfessorBase = Field(
        ...,
        description="The professor who is teaching this course.",
        json_schema_extra={"example": {

        }}
    )
    assignment: List[str] = Field(
        None,
        description="The assignments in this course",
        json_schema_extra={"example": [
            "HW1 is to define and implement two new models, including annotations"
        ]},
    )

    model_config = {
        "json_schema_extra":{
            "examples": [
                {
                    "courseID": "COMS4153",
                    "courseName": "Cloud Computing",
                    "instructor": {
                        "first_name": "John",
                        "last_name": "Smith",
                        "id": "js2233",
                        "email": "js2233@columbia.edu",
                        "courses": ["COMS4153", ]
                    },
                    "assignment": [
                        "HW1 is to define and implement two new models, including annotations",
                    ],
                }
            ]
        }
    }


class CourseCreate(CourseBase):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "courseID": "COMS4153",
                    "courseName": "Cloud Computing",
                    "instructor": {
                        "first_name": "John",
                        "last_name": "Smith",
                        "id": "js2233",
                        "email": "js2233@columbia.edu",
                        "courses": ["COMS4153", ]
                    },
                    "assignment": [
                        "HW1 is to define and implement two new models, including annotations",
                    ],
                },
                {
                    "courseID": "COMS4252",
                    "courseName": "Introduction to Computational Learning",
                    "instructor": {
                        "first_name": "Tony",
                        "last_name": "Li",
                        "id": "tl1122",
                        "email": "tl1122@columbia.edu",
                        "courses": ["COMS4252", ]
                    },
                    "assignment": [
                        "HW1 is to solve Problem Set #1",
                    ],
                }
            ]
        }
    }


class CourseUpdate(BaseModel):
    courseID: Optional[courseIDType] = Field(
        default=None,
        description="The ID of a course.",
        json_schema_extra={"example": "COMS4252"}
    )
    courseName: Optional[str] = Field(
        default=None,
        description="The name of the course.",
        json_schema_extra={"example": "Introduction to Computational Learning Theory"}
    )
    instructor: Optional[ProfessorBase] = Field(
        default=None,
        description="update the professor for this course.",
        json_schema_extra={
            "example": {
                "first_name": "Tony",
                "last_name": "Li",
                "id": "tl2121",
                "email": "tl2121@columbia.edu",
                "courses": ["COMS4252"]
            }
        }
    )
    assignment: Optional[List[str]] = Field(
        default=None,
        description="Replace the entire list of assignments.",
        json_schema_extra={"example": [
            "HW1 is to solve Problem Set #1"
        ]}
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"courseName": "Introduction to Computational Learning"},
                {"instructor": {
                    "first_name": "Tony",
                    "last_name": "Li",
                    "id": "tl2121",
                    "email": "tl2121@columbia.edu",
                    "courses": ["COMS4252"]
                    }
                },
            ]
        }
    }


class CourseRead(CourseBase):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-09-10T14:00:00Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-09-11T10:30:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "courseID": "COMS4153",
                    "courseName": "Cloud Computing",
                    "instructor": {
                        "first_name": "John",
                        "last_name": "Smith",
                        "id": "js2233",
                        "email": "js2233@columbia.edu",
                        "courses": ["COMS4252"],
                    },
                    "assignment": ["HW1: Implement two new models"],
                    "created_at": "2025-09-10T14:00:00Z",
                    "updated_at": "2025-09-11T10:30:00Z",
                }
            ]
        }
    }

