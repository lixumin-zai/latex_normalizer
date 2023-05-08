import logging

from ..exceptions.syntax_exception import LatexSyntaxError

logger = logging.getLogger("base_component")

COMPONENT_MAPPER = {}  # mapper for typestr and Module

class ComponentLogMetaclass(type):
    def __new__(cls, name, bases, attrs):
        global COMPONENT_MAPPER

        class_ = super().__new__(cls, name, bases, attrs)

        main_str = attrs.get('main_str', None)
        if main_str is not None:
            if main_str in COMPONENT_MAPPER:
                logger.warning('Duplicate mian_str for two modules: {}, {}'.format(
                                   COMPONENT_MAPPER[main_str], name))
            COMPONENT_MAPPER[main_str] = class_

        return class_


class BaseComponent(object, metaclass=ComponentLogMetaclass):
    main_str = ''
    _status_dict = {}

    def __init__(self):
        self.sub_component_list = []

    @classmethod
    def match(cls, stream):
        return cls()

    def to_string(self):
        return ''

    def append_sub_component(self, component):
        self.sub_component_list.append(component)

    def extend_sub_component_list(self, component_list: list):
        self.sub_component_list.extend(component_list)

    def get_sub_component_list_in_range(self, left: int, right: int):
        """ Get sub component list given range [left, right)
        """
        return self.sub_component_list[left: right]

    def get_first_sub_component(self):
        if len(self.sub_component_list) == 0:
            raise IndexError("Component {} has no sub "
                             "components".format(self.__class__.__name__))

        return self.sub_component_list[0]

    @classmethod
    def set_status(cls, **kwargs):
        cls._status_dict.update(kwargs)

    @classmethod
    def get_status(cls, key):
        """ Get status of component, return `None` if no such status exists """
        return cls._status_dict.get(key, None)

    def __len__(self):
        return len(self.sub_component_list)

    @classmethod
    def test_token_matched(cls, stream):
        token = stream.peek()
        return token == cls.main_str


class OtherComponent(BaseComponent):
    main_str = 'other'

    def __init__(self, token):
        self.__token = token

    def to_string(self):
        return self.__token

    @classmethod
    def match(cls, stream):
        return cls(stream.read())



