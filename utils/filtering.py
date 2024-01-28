import json
import logging
from inspect import signature
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Extra
from sqlalchemy import func, Select, inspect

from db.setup import Base, get_model_registry


class Operator(object):
    OPERATORS = {
        'is_null': lambda f: f.is_(None),
        'is_not_null': lambda f: f.isnot(None),
        '==': lambda f, a: f == a,
        '!=': lambda f, a: f != a,
        '>': lambda f, a: f > a,
        '<': lambda f, a: f < a,
        '>=': lambda f, a: f >= a,
        '<=': lambda f, a: f <= a,
        'like': lambda f, a: f.like(a),
        'ilike': lambda f, a: f.ilike(a),
        'not_ilike': lambda f, a: ~f.ilike(a),
        'in': lambda f, a: f.in_(a),
        'not_in': lambda f, a: ~f.in_(a),
        'any': lambda f, a: f.any(a),
        'not_any': lambda f, a: func.not_(f.any(a)),
    }

    def __init__(self, operator=None):
        if not operator:
            operator = '=='

        if operator not in self.OPERATORS:
            raise ValueError(f"{operator} is not among supported operators")

        self.operator = operator
        self.function = self.OPERATORS[operator]
        self.arity = len(signature(self.function).parameters)


def get_model_from_table_name(model_name: str):
    """Get model class associated with provided """
    registry = get_model_registry()
    try:
        return registry[model_name]
    except KeyError:
        # leave room for handling exception
        raise


def get_field_from_model(model: Base, field: str):
    if field not in inspect(model).columns.keys():
        raise ValueError(f"Model {model} does not contain column {field}")
    return getattr(model, field)


class BaseFilterSchema(BaseModel):
    model_config = ConfigDict(extra=Extra.ignore)


class FilterJsonSchema(BaseModel):
    field: str
    op: Optional[str] = None
    value: Optional[str | bool] = None


def get_json_filters(filters: Optional[str] = None):
    if filters:
        try:
            loaded_filters = json.loads(filters)
            loaded_filters = [loaded_filters] if isinstance(loaded_filters, dict) else loaded_filters
        except json.JSONDecodeError as e:
            logging.critical(msg=f"Error while trying to decode json filters: {filters}")
            raise e
    else:
        loaded_filters = []
    return [FilterJsonSchema(**f).model_dump() for f in loaded_filters]


def validate_filters(filters: List[dict],
                     validation_schema: BaseFilterSchema) -> List[dict]:
    """Validate filters according to provided validation schema"""
    validated_filters = []
    field_values = {f["field"]: f.get("value") for f in filters}
    validated_filters_obj = validation_schema(**field_values)
    for f in filters:
        if f["field"] in validated_filters_obj.model_fields:
            f["value"] = getattr(validated_filters_obj, f["field"])
            validated_filters.append(f)
    return validated_filters


def apply_filters_to_query(query: Select, model: Base,
                           filters: List[dict], validation_schema: BaseFilterSchema):
    if isinstance(filters, dict):
        filters = [filters]
    validated_filters = validate_filters(filters, validation_schema)
    for f in validated_filters:
        op = Operator(f["op"])
        try:
            field = get_field_from_model(model=model, field=f["field"])
        except ValueError:
            continue
        if op.arity == 1:
            query = query.filter(op.function(field))
        if op.arity == 2:
            query = query.filter(op.function(field, f["value"]))
    return query
