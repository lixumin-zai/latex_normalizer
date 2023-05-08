from .base_component import BaseComponent, OtherComponent
from .component_factory import ComponentFactory
from ..exceptions.syntax_exception import LatexSyntaxError
from ..exceptions.base_exception import InvalidBeginEndType
from ..utils.stream_utils import read_component_until, merge_list_component
from ..stream.token_stream import LatexTokenStream

END_BRACE_SET = {'}', ']', ')'}

class BaseBraceComponent(BaseComponent):
    main_str = "BaseBraceComponent"
    end_sign = ""

    def __init__(self):
        super().__init__()

        self.left = None
        self.right = None

    @classmethod
    def match(cls, stream: LatexTokenStream, strict=False):
        if not cls.test_token_matched(stream):
            return None

        stream.read() # expire first sign

        component = cls()
        end_sign_set = {cls.end_sign} if strict else END_BRACE_SET
        
        component.extend_sub_component_list(
            read_component_until(stream, end_sign_set)
        )
        
        component.right = stream.read() # expire end sign

        return component

    def set_left_sign(self, sign: str):
        self.left = sign

    def set_right_sign(self, sign: str):
        self.right = sign

    def to_string(self, with_head: bool = False):
        if len(self.sub_component_list) == 1 and (
                isinstance(self.sub_component_list[0], type(self))):
            ret_str = self.sub_component_list[0].to_string(with_head=False)
        else:
            ret_str = merge_list_component(self.sub_component_list)
        if with_head:
            ret_str = self.left + ret_str + self.right

        return ret_str


class BraceComponent(BaseBraceComponent):
    main_str = "{"
    end_sign = "}"

    def __init__(self):
        super().__init__()

        self.left = '{'
        self.right = ''

    def to_string(self, with_head: bool = False, 
                  sub_comp_has_outmost_header: bool = True):
        ret_str = merge_list_component(
            self.sub_component_list,
            has_outmost_header=sub_comp_has_outmost_header,
        )
        if with_head:
            ret_str = self.left + ret_str + self.right

        return ret_str


class ParenthesisComponent(BaseBraceComponent):
    main_str = "("
    end_sign = ")"

    def __init__(self):
        super().__init__()

        self.left = "("
        self.right = ""


class SquareBraceComponent(BaseBraceComponent):
    main_str = "["
    end_sign = "]"

    def __init__(self):
        super().__init__()

        self.left = "["
        self.right = ""


class BeginEndComponent(BaseComponent):
    main_str = r"\begin"

    def __init__(self):
        super().__init__()

    @classmethod
    def match(cls, stream: LatexTokenStream):
        if not cls.test_token_matched(stream):
            return None

        stream.read() # expire \beign

        component = cls()

        # Get \begin{}
        begin_type_comp = BraceComponent.match(stream, strict=True)
        component.type_ = begin_type_comp.to_string()
        component.append_sub_component(begin_type_comp)
        
        component.extend_sub_component_list(read_component_until(stream, {r'\end'}))

        stream.read() # expire \end

        component.append_sub_component(BraceComponent.match(stream, strict=True))

        return component

    def to_string(self):
        formular_spliter = []
        for idx, comp in enumerate(self.sub_component_list):
            if isinstance(comp, OtherComponent) and comp.to_string() == '\\\\':
                formular_spliter.append(idx)
        formular_spliter.append(-1)
        
        start_idx = 1 if self.type_ in {'cases', 'matrix'} else 2
        content_list = []
        for split_idx in formular_spliter:
            braced_by_brace = True
            current_sub_comp_list = self.sub_component_list[start_idx:split_idx]
            # No {} if there exists &
            for comp in current_sub_comp_list:
                if (
                    isinstance(comp, ComponentFactory.get_component("other")) 
                        and comp.to_string() == "&"
                ):
                    braced_by_brace = False
                    break

            comp_string = merge_list_component(
                current_sub_comp_list,
                has_outmost_header=False
            )
            if comp_string:
                if braced_by_brace:
                    comp_string = "{" + comp_string + "}"
                content_list.append(comp_string)

            start_idx = split_idx + 1

        if self.type_ in {'cases', 'matrix'}:
            return "\\begin{%(begin_args)s} %(content)s \\end{%(end_args)s}" % {
                "begin_args": self.sub_component_list[0].to_string(),
                "content": ' \\\\ '.join(content_list),
                "end_args": self.sub_component_list[-1].to_string()
            }
        elif self.type_ == 'array':
            return "\\begin{%(begin_args)s}{%(pos)s} %(content)s \\end{%(end_args)s}" % {
                    "begin_args": self.sub_component_list[0].to_string(),
                    "pos": self.sub_component_list[1].to_string(),
                    "content": ' \\\\ '.join(content_list),
                    "end_args": self.sub_component_list[-1].to_string()
                }
        else:
            raise InvalidBeginEndType(
                "Invalid begin end type: {}, only cases, matrix, "
                "array supported".format(self.type_)
            )
        

class AbsComponent(BaseComponent):
    main_str = r"\vert"
    
    def __init__(self):
        super().__init__()

    @classmethod
    def match(cls, stream: LatexTokenStream):
        if not cls.test_token_matched(stream):
            return None

        stream.read() # expire \vect

        component = cls()

        component_list = read_component_until(stream, {cls.main_str})
        component.extend_sub_component_list(component_list)

        stream.read() # expire end \vert

        return component
    
    def to_string(self):
        return "|" + merge_list_component(self.sub_component_list).strip(" ") + "|"

