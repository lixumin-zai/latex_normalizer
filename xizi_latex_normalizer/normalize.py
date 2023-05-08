from .stream import LatexTokenStream
from .components import COMPONENT_MAPPER, OtherComponent, BraceComponent
from .components.component_factory import ComponentFactory
from .exceptions.base_exception import NormalizerException
from .utils.common_utils import trans_chinese_unit_to_latex, split_to_latex_and_not


def normalize_latex_expression(latex: str, 
                               normalize_token: bool = False,
                               ignore_similar_despite_capital: bool = False,
                               keep_left_right_marker: bool = True,
                               strip_angle_for_tri: bool = False,
                               ensure_valid_formula: bool = True,
                               keep_successive_outmost_brace: bool = False,
                               brace_single_elem_for_log: bool = True,
                               keep_rm_sign: bool = True) -> str:
    """ Normalize latex expression to complement brace which could be omitted 
    
    Args:
        latex(str): 
            latex formula expreesion, no $ on both sides
        normalize_token(bool): 
            whether to nomalize token
        ignore_similar_despite_capital(bool): 
            whether to ignore tokens which has similar form for capital case 
            or lower case
        keep_left_right_marker(bool): 
            keep \\left and \\right for formatting
        strip_angle_for_tri(bool): 
            whether to strip \\angle marker for trigonometric function
        ensure_valid_formula(bool): 
            whether guarantee given formula is valid        
        keep_successive_outmost_brace(bool): 
            whether keep successive outest brace,
            for example, if True, {{abc}} -> abc
        brace_single_elem_for_log(bool): 
            whether add brace for logarithm with single element,
            if True, \\log_{2}3 -> \\log_{2}(3),
            otherwise, \\log_{2}(3) -> \\log_{2}3
        keep_rm_sign:
            whether keep \\rm while normalizing,
            if True, \\rm a -> \\rm a,
            otherwise, \\rm a -> a

    Returns:
        str, normalized latex formula, no $ on both sides

    Exceptions:
        Exceptions from NormalizerException: when ensure valid formula is True, and
            syntax error raised, this kind of exception will be raised
    """
    ComponentFactory.set_component_group_status(
        ["\\sin", "\\cos", "\\tan"], "strip_angle", bool(strip_angle_for_tri) 
    )
    ComponentFactory.set_component_group_status(
        ["\\log"], "brace_single_elem", bool(brace_single_elem_for_log)
    )
    ComponentFactory.set_component_group_status(
        ["\\rm"], "keep_rm", bool(keep_rm_sign)
    )

    latex = '{' + latex + '}'
    latex_stream = LatexTokenStream(
        latex, 
        normalize_token=normalize_token,
        ignore_similar_despite_capital=ignore_similar_despite_capital,
        keep_left_right_marker=keep_left_right_marker
    )

    try:
        root_component = BraceComponent.match(latex_stream, strict=True)
        return root_component.to_string(
            sub_comp_has_outmost_header=keep_successive_outmost_brace
        ).strip()

    except NormalizerException as e:
        if ensure_valid_formula:
            raise e

        latex_stream.reset_stream()
        return " ".join(latex_stream.get_all_tokens()[1:-1]).strip()


def normalize_latex_in_sentence(sentence: str, 
                                normalize_token: bool = False,
                                ignore_similar_despite_capital: bool = False,
                                keep_left_right_marker: bool = True,
                                strip_angle_for_tri: bool = False,
                                ensure_valid_formula: bool = True,
                                keep_successive_outmost_brace: bool = False,
                                brace_single_elem_for_log: bool = True,
                                keep_rm_sign: bool = True) -> str:
    """ Normalize all latex expressions in given sentence, the formula needs to be
    branced with $

    Args:
        sentence(str): sentence to be proceesed, latex should be braced with $
        normalize_token(bool): refer to `normalize.normalize_latex_expression`
        ignore_similar_despite_capital(bool): refer to `normalize.normalize_latex_expression`
        keep_left_right_marker(bool): refer to `normalize.normalize_latex_expression`
        strip_angle_for_tri(bool): refer to `normalize.normalize_latex_expression`
        ensure_valid_formula(bool): refer to `normalize.normalize_latex_expression`
        keep_successive_outmost_brace(bool): refer to `normalize.normalize_latex_expression`
        brace_single_elem_for_log(bool): refer to `normalize.normalize_latex_expression`
        keep_rm_sign: refer to `normalize.normalize_latex_expression`

    Returns: 
        str, latex are braced with $

    Exceptions:
        Exceptions from NormalizerException: when ensure valid formula is True, and
            syntax error raised, this kind of exception will be raised
    """
    sentence = trans_chinese_unit_to_latex(sentence)

    sentence_parts = split_to_latex_and_not(sentence)
    for latex_idx, latex in enumerate(sentence_parts[1::2]):
        sentence_parts[2 * latex_idx + 1] = normalize_latex_expression(
            latex, 
            normalize_token=normalize_token,
            ignore_similar_despite_capital=ignore_similar_despite_capital,
            keep_left_right_marker=keep_left_right_marker,
            strip_angle_for_tri=strip_angle_for_tri,
            ensure_valid_formula=ensure_valid_formula,
            keep_successive_outmost_brace=keep_successive_outmost_brace,
            brace_single_elem_for_log=brace_single_elem_for_log,
            keep_rm_sign=keep_rm_sign,
        )
    
    return "$".join(sentence_parts)
