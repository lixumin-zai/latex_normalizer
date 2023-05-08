from .base_component import BaseComponent
from .component_factory import ComponentFactory
from ..stream import LatexTokenStream
from ..utils.stream_utils import merge_list_component


class PrimeComponent(BaseComponent):
    main_str = r"\prime"
    
    @classmethod
    def match(cls, stream: LatexTokenStream):
        if not cls.test_token_matched(stream):
            return None

        component = cls()
        stream.read()

        return component

    def to_string(self, to_quote=False):
        if to_quote:
            return "'"
        else:
            return "\\prime"


class OtherOneSignComponent(BaseComponent):
    main_str = 'other_one_sign'

    def __init__(self, token):
        super().__init__()
        self.__token = token

    def to_string(self):
        return "{}{}".format(
            self.__token, merge_list_component(self.sub_component_list)
        )

    @classmethod
    def match(cls, stream):
        # read first char
        comp = cls(stream.read_one_char())

        to_test_comp_set = {
            ComponentFactory.get_component("^"),
            ComponentFactory.get_component("_"),
        }

        for _ in range(2):
            for to_test_comp in to_test_comp_set:
                match_result = to_test_comp.match(stream)
                if match_result is not None:
                    to_test_comp_set.remove(to_test_comp)
                    comp.append_sub_component(match_result)
                    break

        return comp


class OneSignComponent(BaseComponent):
    main_str = 'one_sign'

    def __init__(self, token):
        super().__init__()
        self.__token = token

    def to_string(self):
        return self.__token

    @classmethod
    def match(cls, stream):
        return cls(stream.read_one_char())

