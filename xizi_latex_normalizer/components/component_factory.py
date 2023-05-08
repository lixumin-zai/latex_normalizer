import pprint

from . import (
    COMPONENT_MAPPER, OtherComponent
)
from ..exceptions.base_exception import InvalidMainstrException


class ComponentFactory(object):
    def __init__(self):
        super().__init__()

    @classmethod
    def get_component(cls, main_str):
        return COMPONENT_MAPPER.get(main_str, OtherComponent)

    @classmethod
    def get_matched_component(cls, stream):
        for Comp in COMPONENT_MAPPER.values():
            if Comp == OtherComponent:
                continue
            if Comp.test_token_matched(stream):
                return Comp

        return OtherComponent

    @classmethod
    def set_component_group_status(cls, main_str_list: list, status, value):
        for str_ in main_str_list:
            if str_ not in COMPONENT_MAPPER:
                raise InvalidMainstrException("No component as "
                                              "main_str: {}".format(str_))

            comp = cls.get_component(main_str=str_)
            comp.set_status(**{status: value})
