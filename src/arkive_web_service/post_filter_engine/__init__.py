from typing import List

import sqlalchemy

from .types import (
    GetAllRequestSort,
    GetAllRequestSortDirection,
    GetAllRequestWhere,
    GetAllRequestWhereFieldType,
    GetAllRequestWhereOperator,
)


def get_sqlalchemy_filter_clause(where: List[GetAllRequestWhere]):
    clauses = []
    for w in where:
        field = w.field
        value = field.parse_value_to_python(w.value)
        if field.type_ == GetAllRequestWhereFieldType.datetime:
            if w.operator == GetAllRequestWhereOperator.gt:
                clauses.append(sqlalchemy.column(field.name) > value)
            elif w.operator == GetAllRequestWhereOperator.lt:
                clauses.append(sqlalchemy.column(field.name) < value)
            elif w.operator == GetAllRequestWhereOperator.gte:
                clauses.append(sqlalchemy.column(field.name) >= value)
            elif w.operator == GetAllRequestWhereOperator.lte:
                clauses.append(sqlalchemy.column(field.name) <= value)
            else:
                raise ValueError("Invalid operator")
    return clauses


def get_sqlalchemy_sort_clause(sort: GetAllRequestSort):
    return (
        sqlalchemy.column(sort.field).asc()
        if sort.direction == GetAllRequestSortDirection.asc
        else sqlalchemy.column(sort.field).desc()
    )
