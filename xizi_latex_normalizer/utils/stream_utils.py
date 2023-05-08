from ..components.component_factory import ComponentFactory
from ..exceptions.syntax_exception import LatexSyntaxError
from ..stream import LatexTokenStream


def read_component(latex_stream: LatexTokenStream):
    """ Expire one component in `latex_stream` """
    component_cls = ComponentFactory.get_matched_component(latex_stream)
    return component_cls.match(latex_stream)


def read_component_until(stream: LatexTokenStream, sign_set):
    """ Iteratively read components. After retrieving, the stream will currently
    points to `sign`
    """
    component_obj_list = []

    token = stream.peek()
    while token is not None and token not in sign_set:
        component_obj_list.append(
            ComponentFactory.get_component(token).match(stream)
        )
        token = stream.peek()

    if token is None:
        raise LatexSyntaxError("Latex: {}, No matched sign for {} found".format(
                                    stream.get_stream_str(), ','.join(sign_set)))
        
    return component_obj_list


def merge_list_component(component_list: list, 
                         has_outmost_header=True,
                         header_for_brace_component=True,
                         header_for_only_brace_component=False):
    if len(component_list) == 0:
        return ''

    normalize_exp_and_sub_seq(component_list)

    ret = []
    for idx, comp in enumerate(component_list):
        kwargs = {}

        interval_sign = ' ' if idx else ''
        if isinstance(comp, (
            ComponentFactory.get_component('^'),
            ComponentFactory.get_component('_'),
            ComponentFactory.get_component('\\circ'),
            ComponentFactory.get_component('\\degree'),
        )):
            interval_sign = ''

        if header_for_brace_component and issubclass(
            type(comp), ComponentFactory.get_component('BaseBraceComponent')):

            kwargs['with_head'] = True

            if not has_outmost_header and len(component_list) == 1:
                # Only BraceComponent support strip outmost header
                if isinstance(comp, ComponentFactory.get_component("{")):
                    kwargs['with_head'] = False
                    kwargs['sub_comp_has_outmost_header'] = has_outmost_header

        if not header_for_only_brace_component and isinstance(
                comp, ComponentFactory.get_component('{')):
            kwargs['with_head'] = False

        ret.append(interval_sign + comp.to_string(**kwargs))

    return ''.join(ret)
        

def normalize_exp_and_sub_seq(component_list: list):
    idx = 0
    while idx < len(component_list) - 1:
        if (
            isinstance(component_list[idx], ComponentFactory.get_component("^")) and
            isinstance(component_list[idx+1], ComponentFactory.get_component("_"))
        ):
            swap_list_item(component_list, idx, idx+1)
            idx += 1
        idx += 1
        
    return component_list


def swap_list_item(list_: list, idx1, idx2):
    tmp = list_[idx1]
    list_[idx1] = list_[idx2]
    list_[idx2] = tmp
    