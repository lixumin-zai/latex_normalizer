import re

from .base_component import BaseComponent
from .component_factory import ComponentFactory
from ..exceptions.base_exception import InvalidComponentException
from ..exceptions.syntax_exception import LatexSyntaxError
from ..stream import LatexTokenStream
from ..utils.stream_utils import read_component, normalize_exp_and_sub_seq


special_tokens = [
    "π", "\\pi", "\\beta", "\\alpha", "\\sigma", "\\phi", "\\Phi", "\\theta",
    "\\gamma", "\\delta", "\\epsilon", "\\varepsilon", "\\zeta", "\\eta", "\\rho",
    "\\lambda", "\\mu", "\\xi", "\\phi", "\\psi", "\\omega",
]


class SqrtComponent(BaseComponent):
    main_str = r"\sqrt"

    def __init__(self):
        super(SqrtComponent, self).__init__()

    @classmethod
    def match(cls, stream: LatexTokenStream):
        if not cls.test_token_matched(stream):
            return None

        component = cls()
        
        stream.read() # expire \sqrt
        
        # Get [] component
        rad_exp_comp = ComponentFactory.get_component("[").match(stream)
        if rad_exp_comp is not None:
            component.append_sub_component(rad_exp_comp)

        if stream.peek_one_char().isalnum():
            component.append_sub_component(
                ComponentFactory.get_component('one_sign').match(stream)
            )
        else:
            component.append_sub_component(read_component(stream))

        return component
        
    def to_string(self):
        if len(self.sub_component_list) == 1:
            return '%(main_str)s{%(root)s}' % {
                'main_str': self.main_str,
                'root': self.sub_component_list[0].to_string()
            }
        elif len(self.sub_component_list) == 2:
            return '%(main_str)s[%(rad_exp)s]{%(root)s}' % {
                'main_str': self.main_str,
                'rad_exp': self.sub_component_list[0].to_string(),
                'root': self.sub_component_list[1].to_string()
            }
        else:
            raise LatexSyntaxError("Latex: {}: Too many subcomponents for frac, "
                                   "expected 1 or 2, get: {}".format(
                                       stream.get_stream_str(), 
                                       len(self.sub_component_list)))


class MoninalComponent(BaseComponent):
    main_str = "moninal"
    match_str = r"^([0-9 ]*([ a-zA-Z]|π|\\pi|\\beta|\\alpha|\\sigma|\\phi|\\Phi|\\theta|\\gamma|\\delta|\\epsilon|\\varepsilon|\\zeta|\\eta|\\rho|\\lambda|\\mu|\\xi|\\phi|\\psi|\\omega)+|[0-9]\s*\.[0-9 ]+|[0-9]+)"

    @classmethod
    def test_token_matched(cls, stream):
        return stream.peek_with_re(cls.match_str) is not None

    @classmethod
    def match(cls, stream: LatexTokenStream):
        if not cls.test_token_matched(stream):
            return None

        component = cls()
        component.append_sub_component(
            ComponentFactory.get_component("other")(
                stream.read_with_re(cls.match_str)
            )
        )

        to_test_comp_list = [
            ComponentFactory.get_component("^"),
            ComponentFactory.get_component("_"),
        ]

        comp_list = []
        for _ in range(2):
            for to_test_comp in to_test_comp_list:
                match_result = to_test_comp.match(stream)
                if match_result is not None:
                    component.append_sub_component(match_result)

        if len(comp_list) == 0:
            pass
        elif len(comp_list) == 1:
            component.append_sub_component(comp_list[0])
        elif len(comp_list) == 2:
            if isinstance(comp_list[0], ComponentFactory.get_component("^")):
                component.append_sub_component(comp_list[1])
                component.append_sub_component(comp_list[0])
            else:
                component.append_sub_component(comp_list[0])
                component.append_sub_component(comp_list[1])
        else:
            raise LatexSyntaxError(
                "Latex: {} has more than 2 consecutive sup/sub".format(
                    stream.get_stream_str())
            )

        return component

    def to_string(self):
        value = "".join([comp.to_string() for comp in self.sub_component_list])

        _stream, token_list = LatexTokenStream(value), []
        tokenized_list = _stream.tokenize()
        for idx, token in enumerate(tokenized_list):
            if re.match(r"\\[a-zA-Z]+", token) and (
                len(tokenized_list) != 1 and idx != len(tokenized_list) - 1
            ):
                token_list.append(token + " ")
            else:
                if not re.match(r"[a-zA-Z0-9]+", token) and token_list:
                    token_list[-1] = token_list[-1].strip()
                
                token_list.append(token.strip())

        return '%(value)s' % {
            'value': "".join(token_list) 
        }


class LogrithmComponent(BaseComponent):
    main_str = "\\log"

    @classmethod
    def match(cls, stream, allow_sub=True):
        if not cls.test_token_matched(stream):
            return None

        component = cls()
        
        stream.read() # expire \\log

        # check if logarith has sup before sub 
        sup_comp = ComponentFactory.get_component("^").match(stream)
        if sup_comp is not None:
            component.append_sub_component(sup_comp)

        if allow_sub:
            # Test if exists subscript
            subscript_component = ComponentFactory.get_component("_").match(stream)
            if subscript_component is not None:
                component.append_sub_component(subscript_component)

        # Recheck if logarith has sup
        if sup_comp is None:
            comp = ComponentFactory.get_component("^").match(stream)
            if comp is not None:
                component.append_sub_component(comp)

        # Get Value
        sub_component = None
        test_components = [
            ComponentFactory.get_component("("),
            ComponentFactory.get_component("{"),
            ComponentFactory.get_component("moninal")
        ]
        for comp in test_components:
            sub_component = comp.match(stream)
            if sub_component is None:
                continue

            if isinstance(sub_component, ComponentFactory.get_component("{")):
                sub_component.set_left_sign("(")
                sub_component.set_right_sign(")")
            elif isinstance(sub_component, ComponentFactory.get_component("(")):
                # 20221031: 额外考虑括号还带上指数的情况
                _sup_comp = ComponentFactory.get_component("^").match(stream)
                if _sup_comp is not None:
                    _sub_component = ComponentFactory.get_component("(")()
                    _sub_component.right = ")"
                    _sub_component.append_sub_component(sub_component)
                    _sub_component.append_sub_component(_sup_comp)
                    sub_component = _sub_component

            break

        if sub_component is None:
            raise InvalidComponentException("No component following "
                                            "{}".format(cls.__name__))

        component.append_sub_component(sub_component)

        if len(component.sub_component_list) > 3:
            raise LatexSyntaxError("Latex: {}, To many components for {}, "
                                   "expected 1/2/3, get: {}".format(
                                       stream.get_stream_str(),
                                       cls.__name__, 
                                       len(component.sub_component_list)))
        
        return component

    def to_string(self):
        if len(self.sub_component_list) == 1:
            return '%(main_str)s(%(value)s)' % {
                'main_str': self.main_str,
                'value': self.sub_component_list[0].to_string()
            }
        elif len(self.sub_component_list) == 2:
            test_comp = self.sub_component_list[1]
            if issubclass(type(test_comp), 
                          ComponentFactory.get_component("BaseBraceComponent")):
                if len(test_comp.sub_component_list) == 1:
                    test_comp = test_comp.sub_component_list[0]
 
            if (isinstance(test_comp, (ComponentFactory.get_component("other"),
                                      ComponentFactory.get_component("other_one_sign"),
                                      ComponentFactory.get_component("moninal")))
                    and not self.get_status("brace_single_elem")):
                return '%(main_str)s%(sub)s%(value)s' % {
                    'main_str': self.main_str,
                    "sub": self.sub_component_list[0].to_string(),
                    'value': self.sub_component_list[1].to_string()
                }
            
            return '%(main_str)s%(sub)s(%(value)s)' % {
                'main_str': self.main_str,
                "sub": self.sub_component_list[0].to_string(),
                'value': self.sub_component_list[1].to_string()
            }
        elif len(self.sub_component_list) == 3:
            normalize_exp_and_sub_seq(self.sub_component_list)
            return '%(main_str)s%(sub)s%(sup)s(%(value)s)' % {
                'main_str': self.main_str,
                "sub": self.sub_component_list[0].to_string(),
                "sup": self.sub_component_list[1].to_string(),
                'value': self.sub_component_list[2].to_string()
            }


class LgComponent(LogrithmComponent):
    main_str = "\\lg"

    @classmethod
    def match(cls, stream):
        return super().match(stream, allow_sub=False)


class LnComponent(LogrithmComponent):
    main_str = "\\ln"

    @classmethod
    def match(cls, stream):
        return super().match(stream, allow_sub=False)


class AngleComponent(BaseComponent):
    main_str = "\\angle"
    
    @classmethod
    def match(cls, stream: LatexTokenStream):
        if not cls.test_token_matched(stream):
            return None

        component = cls()
        
        stream.read() # expire \\angle
        
        value_comp = read_component(stream) 
        if value_comp is None:
            raise LatexSyntaxError("Latex:{}, Values are required following "
                                   "\\angle".format(stream.get_stream_str()))

        component.append_sub_component(value_comp)

        return component
        

    def to_string(self, with_angle_marker=True):
        if with_angle_marker:
            return "%(main_str)s %(value)s" % {
                "main_str": self.main_str,
                "value": self.sub_component_list[0].to_string()
            }
        else:
            return "%(value)s" % {
                "value": self.sub_component_list[0].to_string()
            }


class ExpComponent(BaseComponent):
    main_str = r"^"

    def __init__(self):
        super().__init__()

    @classmethod
    def match(cls, stream: LatexTokenStream):
        if not cls.test_token_matched(stream):
            return None

        component = cls()
        
        stream.read() # expire ^
        
        if stream.peek_one_char().isalnum():
            component.append_sub_component(
                ComponentFactory.get_component("one_sign").match(stream)
            )
        else:
            component.append_sub_component(read_component(stream))

        return component

    def _should_disbale_exp_for_circ(self):
        test_component = self.sub_component_list[0]
        kwargs = {}
        if isinstance(test_component, ComponentFactory.get_component("{")):
            if len(test_component.sub_component_list) == 1:
                if isinstance(test_component.sub_component_list[0] , 
                              (CircComponent, DegreeComponent)):
                    test_component = test_component.sub_component_list[0]

        return (
            isinstance(test_component, (CircComponent, DegreeComponent)), 
            test_component,
            kwargs,
        )

    def _is_all_prime(self):
        test_comp = self.sub_component_list[0]
        if isinstance(test_comp, ComponentFactory.get_component("\\prime")):
            return True
        elif isinstance(test_comp, ComponentFactory.get_component("{")):
            for sub_comp in test_comp.sub_component_list:
                if not isinstance(sub_comp, 
                                  ComponentFactory.get_component("\\prime")):
                    return False

            return True
        return False

    def _to_string_for_all_prime(self):
        test_comp = self.sub_component_list[0]
        if isinstance(test_comp, ComponentFactory.get_component("\\prime")):
            return test_comp.to_string(to_quote=True)
        elif isinstance(test_comp, ComponentFactory.get_component("{")):
            prime_list = []
            for sub_comp in test_comp.sub_component_list:
                prime_list.append(sub_comp.to_string(to_quote=True))
            
            return "".join(prime_list)

    def to_string(self):
        disable, component, kwargs = self._should_disbale_exp_for_circ()
        all_prime = False
        if disable:
            value = component.to_string(with_sup=False)
        elif self._is_all_prime():
            all_prime = True
            value = self._to_string_for_all_prime()
        else:
            value = component.to_string(**kwargs)

        if all_prime:
            return value
        else:
            return '%(main_str)s{%(value)s}' % {
                'main_str': self.main_str,
                'value': value
            }


class SubscriptComponent(BaseComponent):
    main_str = r"_"

    def __init__(self):
        super().__init__()

    @classmethod
    def match(cls, stream: LatexTokenStream):
        if not cls.test_token_matched(stream):
            return None

        component = cls()
        
        stream.read() # expire ^
        
        if stream.peek_one_char().isalnum():
            component.append_sub_component(
                ComponentFactory.get_component("one_sign").match(stream)
            )
        else:
            component.append_sub_component(read_component(stream))

        return component

    def to_string(self):
        return '%(main_str)s{%(value)s}' % {
            'main_str': self.main_str,
            'value': self.sub_component_list[0].to_string()
        }


class VectorComponent(BaseComponent):
    main_str = r"\vec"

    def __init__(self):
        super().__init__()

    @classmethod
    def match(cls, stream: LatexTokenStream):
        if not cls.test_token_matched(stream):
            return None

        component = cls()
        
        stream.read() # expire ^
        
        if stream.peek_one_char().isalnum():
            component.append_sub_component(
                ComponentFactory.get_component("other_one_sign").match(stream)
            )
        else:
            component.append_sub_component(read_component(stream))

        return component

    def to_string(self):
        return '%(main_str)s{%(value)s}' % {
            'main_str': self.main_str,
            'value': self.sub_component_list[0].to_string()
        }


class Vector2Component(VectorComponent):
    main_str = r"\textbf"


class Vector3Component(VectorComponent):
    main_str = r"\boldsymbol"


class TrigonometricFunctionComponent(BaseComponent):
    main_str = 'trigonometric function'
    def __init__(self):
        super().__init__()

    @classmethod
    def match(cls, stream):
        if not cls.test_token_matched(stream):
            return None

        component = cls()
        
        stream.read() # expire main_str

        # enable status
        if component.get_status("strip_angle"):
            stream.enable_strip_angle()
        
        # If there are sup operation, it should be combined with \sin
        comp = ComponentFactory.get_component("^").match(stream)
        if comp is not None:
            component.append_sub_component(comp)

        sub_component = None
        test_components = [
            ComponentFactory.get_component("("),
            ComponentFactory.get_component("{"),
            ComponentFactory.get_component("moninal"),
            ComponentFactory.get_component("\\frac"),
        ]
        for comp in test_components:
            sub_component = comp.match(stream)
            if sub_component is None:
                continue

            if isinstance(sub_component, ComponentFactory.get_component("{")):
                sub_component.set_left_sign("(")
                sub_component.set_right_sign(")")

            if isinstance(sub_component, ComponentFactory.get_component("\\frac")):
                _comp = ComponentFactory.get_component("BaseBraceComponent")()
                _comp.append_sub_component(sub_component)

                if stream.peek() in special_tokens:
                    _comp.append_sub_component(
                        ComponentFactory.get_component("other")(stream.read())
                    )

                sub_component = _comp

            break

        if sub_component is None:
            sub_component = read_component(stream)

        if sub_component is None:
            raise InvalidComponentException("No component following "
                                            "{}".format(cls.__name__))

        component.append_sub_component(sub_component)

        # disable status and avoid overwrite origin status
        if component.get_status("strip_angle"):
            stream.disable_strip_angle()

        return component

    def to_string(self):

        if len(self.sub_component_list) == 1:
            kwargs = {}
            if isinstance(self.sub_component_list[0], 
                          ComponentFactory.get_component("(")):
                kwargs["with_head"] = False

            return '%(main_str)s(%(value)s)' % {
                'main_str': self.main_str,
                'value': self.sub_component_list[0].to_string()
            }
        elif len(self.sub_component_list) == 2:
            return '%(main_str)s%(operation)s(%(value)s)' % {
                'main_str': self.main_str,
                'operation': self.sub_component_list[0].to_string(),
                'value': self.sub_component_list[1].to_string()
            }
        else:
            raise LatexSyntaxError("More than 2 sub_component for sup operation")


class SineFunctionComponent(TrigonometricFunctionComponent):
    main_str = "\\sin"


class CscFunctionComponent(TrigonometricFunctionComponent):
    main_str = "\\csc"


class SecFunctionComponent(TrigonometricFunctionComponent):
    main_str = "\\sec"


class CotFunctionComponent(TrigonometricFunctionComponent):
    main_str = "\\cot"


class ArcSineFunctionComponent(TrigonometricFunctionComponent):
    main_str = "\\arcsin"


class ArcCosFunctionComponent(TrigonometricFunctionComponent):
    main_str = "\\arccos"


class ArcTanFunctionComponent(TrigonometricFunctionComponent):
    main_str = "\\arctan"


class ArcCscFunctionComponent(TrigonometricFunctionComponent):
    main_str = "\\arccsc"


class ArcSecFunctionComponent(TrigonometricFunctionComponent):
    main_str = "\\arcsec"


class ArcCotFunctionComponent(TrigonometricFunctionComponent):
    main_str = "\\arccot"


class SinhFunctionComponent(TrigonometricFunctionComponent):
    main_str = "\\sinh"


class CoshFunctionComponent(TrigonometricFunctionComponent):
    main_str = "\\cosh"


class TanhFunctionComponent(TrigonometricFunctionComponent):
    main_str = "\\tanh"


class CschFunctionComponent(TrigonometricFunctionComponent):
    main_str = "\\csch"


class SechFunctionComponent(TrigonometricFunctionComponent):
    main_str = "\\sech"


class CothFunctionComponent(TrigonometricFunctionComponent):
    main_str = "\\coth"


class ArcSinhFunctionComponent(TrigonometricFunctionComponent):
    main_str = "\\arsinh"


class ArcCoshFunctionComponent(TrigonometricFunctionComponent):
    main_str = "\\arcosh"


class ArcTanhFunctionComponent(TrigonometricFunctionComponent):
    main_str = "\\artanh"


class ArcCschFunctionComponent(TrigonometricFunctionComponent):
    main_str = "\\arccsch"


class ArcSechFunctionComponent(TrigonometricFunctionComponent):
    main_str = "\\arcsech"


class ArcCothFunctionComponent(TrigonometricFunctionComponent):
    main_str = "\\arccoth"


class CosineFunctionComponent(TrigonometricFunctionComponent):
    main_str = "\\cos"


class TangentFunctionComponent(TrigonometricFunctionComponent):
    main_str = "\\tan"


class RmComponent(BaseComponent):
    main_str = r'\rm'

    @classmethod
    def match(cls, stream):
        if not cls.test_token_matched(stream):
            return None

        component = cls()
        
        stream.read() # expire main_str
        
        brace_component = ComponentFactory.get_component("{").match(stream)

        if brace_component is not None:
            component.append_sub_component(brace_component)

        return component

    def to_string(self):
        if self.sub_component_list:
            if self.get_status("keep_rm"):
                return '%(main_str)s %(value)s' % {
                    "main_str": self.main_str,
                    'value': self.sub_component_list[0].to_string(),
                }
            else:
                return '%(value)s' % {
                    'value': self.sub_component_list[0].to_string()
                }
        else:
            return self.main_str if self.get_status("keep_rm") else ""
        

class CircComponent(BaseComponent):
    main_str = r'\circ'

    @classmethod
    def match(cls, stream):
        if not cls.test_token_matched(stream):
            return None

        component = cls()
        
        component.append_sub_component(
            ComponentFactory.get_component("other")(stream.read())
        )

        return component

    def to_string(self, with_sup=True):
        format_str = "%(value)s"
        if with_sup:
            format_str = "^{%(value)s}"

        return format_str % {
            'value': self.sub_component_list[0].to_string()
        }
        
        
class DegreeComponent(CircComponent):
    main_str = r'\degree'


class OverlineComponent(BaseComponent):
    main_str = r'\overline'

    @classmethod
    def match(cls, stream):
        if not cls.test_token_matched(stream):
            return None

        component = cls()
        
        stream.read() # expire main_str
        
        brace_component = ComponentFactory.get_component("{").match(stream)
        if brace_component is not None:
            component.append_sub_component(brace_component)
        else:
            other_component = ComponentFactory.get_component(
                "other_one_sign").match(stream)
            if other_component is not None:
                component.append_sub_component(other_component)
            else:
                raise LatexSyntaxError

        return component

    def to_string(self):
        return "%(main_str)s{%(value)s}" % {
            "main_str": self.main_str,
            "value": self.sub_component_list[0].to_string(),
        }
