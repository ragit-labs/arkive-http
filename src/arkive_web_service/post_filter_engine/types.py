from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class GetAllRequestWhereOperator(str, Enum):
    gt = "gt"
    lt = "lt"
    gte = "gte"
    lte = "lte"


class GetAllRequestWhereFieldType(str, Enum):
    datetime = "datetime"


class GetAllRequestWhereField(BaseModel):
    name: str
    type_: GetAllRequestWhereFieldType = Field(title="Type of the value", alias="type")

    def parse_value_to_python(self, value: str):
        if self.type_ == GetAllRequestWhereFieldType.datetime:
            return datetime.fromisoformat(value)


class GetAllRequestWhere(BaseModel):
    field: GetAllRequestWhereField
    value: str
    operator: GetAllRequestWhereOperator


class GetAllRequestSortDirection(str, Enum):
    asc = "asc"
    desc = "desc"


class GetAllRequestSort(BaseModel):
    field: str
    direction: GetAllRequestSortDirection


class GetAllRequest(BaseModel):
    where: Optional[List[GetAllRequestWhere]] = Field(None, title="Where clause")
    tags: Optional[List[str]] = Field(None, title="Tags to filter by")
    sort: Optional[GetAllRequestSort] = Field(None, title="Sort by")
    limit: Optional[int] = Field(None, title="Limit the number of results")
    skip: Optional[int] = Field(None, title="Skip the first n results")
