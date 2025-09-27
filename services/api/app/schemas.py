from typing import Any, Literal

from pydantic import BaseModel, Field


class EnqueueRequest(BaseModel):
    type: Literal["add", "heavy"] = "add"
    params: dict[str, Any] = Field(default_factory=dict)
    queue: Literal["high", "default", "low"] = "default"


class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    result: Any | None = None
