from .base_component import BaseComponent
from .component_factory import ComponentFactory
from ..exceptions.syntax_exception import LatexSyntaxError
from ..stream import LatexTokenStream
from ..utils.stream_utils import read_component


class FracComponent(BaseComponent):
    main_str = r"\frac"

    def __init__(self):
        super(FracComponent, self).__init__()

    @classmethod
    def match(cls, stream: LatexTokenStream):
        if not cls.test_token_matched(stream):
            return None

        component = cls()
        stream.read() # expire \frac

        for _ in range(2):
            if stream.peek_one_char().isalnum():
                component.append_sub_component(
                    ComponentFactory.get_component("other_one_sign").match(stream)
                )
            else:
                component.append_sub_component(read_component(stream))

        if len(component.sub_component_list) != 2:
            raise LatexSyntaxError("Latex: {}, Too many subcomponents for frac, "
                                   "expected 2 or 3, get: {}".format(
                                       stream.get_stream_str(), 
                                       len(component.sub_component_list)))

        return component
        
    def to_string(self):
        if len(self.sub_component_list) == 2:
            return '%(main_str)s{%(nominator)s}{%(denominator)s}' % {
                "main_str": self.main_str,
                "nominator": self.sub_component_list[0].to_string(),
                "denominator": self.sub_component_list[1].to_string()
            }

        return super().to_string()


class DFracComponent(FracComponent):
    main_str = r"\dfrac"


class OversetComponent(BaseComponent):
    main_str = r"\overset"

    def __init__(self):
        super(OversetComponent, self).__init__()

    @classmethod
    def match(cls, stream: LatexTokenStream):
        if not cls.test_token_matched(stream):
            return None

        component = cls()
        stream.read() # expire \overset

        for _ in range(2):
            if stream.peek_one_char().isalnum():
                component.append_sub_component(
                    ComponentFactory.get_component("other_one_sign").match(stream)
                )
            else:
                component.append_sub_component(read_component(stream))

        if len(component.sub_component_list) != 2:
            raise LatexSyntaxError("Latex: {}, Too many subcomponents for frac, "
                                   "expected 2 or 3, get: {}".format(
                                       stream.get_stream_str(), 
                                       len(component.sub_component_list)))
        return component
        
    def to_string(self):
        if len(self.sub_component_list) == 2:
            return '%(main_str)s{%(nominator)s}{%(denominator)s}' % {
                "main_str": self.main_str,
                "nominator": self.sub_component_list[0].to_string(),
                "denominator": self.sub_component_list[1].to_string()
            }

        return super().to_string()


class UndersetComponent(OversetComponent):
    main_str = r"\underset"

    def __init__(self):
        super().__init__()


class ComplementComponent(BaseComponent):
    main_str = r"\complement"

    def __init__(self):
        super(ComplementComponent, self).__init__()

    @classmethod
    def match(cls, stream: LatexTokenStream):
        if not cls.test_token_matched(stream):
            return None

        component = cls()
        stream.read() # expire \complement

        subscript_comp = ComponentFactory.get_component("_").match(stream)
        if subscript_comp is not None:
            component.append_sub_component(subscript_comp)

        component.append_sub_component(read_component(stream))

        return component
        
    def to_string(self):
        if len(self.sub_component_list) == 1:
            return '%(main_str)s{%(complement)s}' % {
                "main_str": self.main_str,
                "complement": self.sub_component_list[0].to_string()
            }
        elif len(self.sub_component_list) == 2:
            return '%(main_str)s%(full)s{%(complement)s}' % {
                "main_str": self.main_str,
                "full": self.sub_component_list[0].to_string(),
                "complement": self.sub_component_list[1].to_string(),
            }

        return super().to_string()
