from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class PostDeleteRequestData(BaseModel):
    post_id: str


class PostInsertRequestData(BaseModel):
    title: str = Field(..., title="Title of the post")
    content: str = Field(..., title="Content of the post")
    url: str = Field(..., title="URL of the post")
    banner: Optional[str] = Field(None, title="Banner image URL")
    timestamp: datetime = Field(..., title="Timestamp of the post")
    extra_metadata: Optional[dict] = Field(None, title="Extra metadata")
    tags: List[str] = Field(..., title="Tags for the post")
    user_id: str = Field(..., title="User id")
