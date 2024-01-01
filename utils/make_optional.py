import inspect
from typing import Optional

from pydantic import create_model, BaseModel, Field, ConfigDict
from pydantic.fields import FieldInfo


class TestModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int = Field(ge=1)
    name: str
    age: int


def optional(model: BaseModel, fields: Optional[list] = None):
    """
    Decorator transforming all or specified fields of given model to Optional.
    Modified version of code snippet submitted by user mubtasimfuad on GitHub:
    https://github.com/pydantic/pydantic/issues/1223#issuecomment-1633592384
    :param fields:
    :return:
    """

    def dec(cls: BaseModel):
        fields_dict = {}
        for field in fields:
            field_info = FieldInfo(default=None,
                                   annotation=cls.model_fields.get(field).annotation)
            if field_info is not None:
                fields_dict[field] = (Optional[field_info.annotation], field_info)
        OptionalModel = create_model(cls.__name__, **fields_dict, __config__=cls.model_config)
        OptionalModel.__module__ = cls.__module__

        return OptionalModel

    if model:
        cls = model
        fields = fields if fields else cls.model_fields.keys()
        return dec(cls)

    return dec


def test_make_optional():
    OptionalTestModel = optional(TestModel)
    ot = OptionalTestModel(id=-1, name='dev', age=None)
