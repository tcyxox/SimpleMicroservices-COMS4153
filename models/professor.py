from __future__ import annotations

from typing import Optional, List, Annotated
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import Field, StringConstraints, EmailStr, BaseModel

idType = Annotated[str, StringConstraints(pattern=r"^[a-z]{2,3}\d{1,4}$")]
courseIDType = Annotated[str, StringConstraints(pattern=r"^[A-Z]{4}\d{4}$")]


class ProfessorBase(BaseModel):
    first_name: str = Field(
        ...,
        description="First name of the professor",
        json_schema_extra={"example": "John"},
    )
    last_name: str = Field(
        ...,
        description="Last name of the professor",
        json_schema_extra={"example": "Smith"},
    )
    id: idType = Field(
        ...,
        description="The only ID of the professor in Columbia",
        json_schema_extra={"example": "ab1234"},
    )
    email: EmailStr = Field(
        ...,
        description="Professor's email address",
        json_schema_extra={"example": "xxx@columbia.edu"},
    )
    courses: List[courseIDType] = Field(
        default_factory=List,
        description="The ID of courses that the professor is teaching.",
        json_schema_extra={"examples": ["COMS4252",]}
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "first_name": "John",
                    "last_name": "Smith",
                    "id": "js2233",
                    "email": "js2233@columbia.edu",
                    "courses": ["COMS4252",]
                }
            ]
        }
    }


class ProfessorCreate(ProfessorBase):
    """Creation payload for a Professor."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "first_name": "Tony",
                    "last_name": "Li",
                    "id": "tl2121",
                    "email": "tl2121@columbia.edu",
                    "courses": ["COMS4115", "COMS6115"],
                },
                {
                    "first_name": "John",
                    "last_name": "Smith",
                    "id": "js2233",
                    "email": "js2233@columbia.edu",
                    "courses": ["COMS4252", ]
                }
            ]
        }
    }


class ProfessorUpdate(BaseModel):
    """Partial update for a Professor; supply only fields to change."""
    first_name: Optional[str] = Field(
        None,
        description="First name of the professor",
        json_schema_extra={"example": "Jon"},
    )
    last_name: Optional[str] = Field(
        None,
        description="Last name of the professor",
        json_schema_extra={"example": "Smyth"},
    )
    id: Optional[idType] = Field(
        None,
        description="The only ID of the professor in Columbia",
        json_schema_extra={"example": "js1234"},
    )
    email: Optional[EmailStr] = Field(
        None,
        description="Professor's email address",
        json_schema_extra={"example": "john.smith@columbia.edu"},
    )
    courses: Optional[List[courseIDType]] = Field(
        None,
        description="Replace the entire set of courses with this list.",
        json_schema_extra={"example": ["COMS6998"]},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"last_name": "Doe"},
                {
                    "email": "js2233@cs.columbia.edu",
                    "courses": ["COMS4252", "COMS4004"],
                },
            ]
        }
    }


class ProfessorRead(ProfessorBase):
    """Server representation returned to clients."""
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-02-20T11:22:33Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-02-21T13:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "first_name": "John",
                    "last_name": "Smith",
                    "id": "js2233",
                    "email": "js2233@columbia.edu",
                    "courses": ["COMS4252"],
                    "created_at": "2025-02-20T11:22:33Z",
                    "updated_at": "2025-02-21T13:00:00Z",
                }
            ]
        }
    }
