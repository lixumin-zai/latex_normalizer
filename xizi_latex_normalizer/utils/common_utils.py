from collections import OrderedDict
import re


# 所有中文单位列表
CHINESE_UNIT_TO_LATEX_MAPPER = OrderedDict(
    米="m", 厘米="cm", 分米="dm", 毫米="mm", 千米="km",
    平方米="m^2", 平方厘米="cm^2", 平方毫米="mm^2", 平方千米="km^2",
    立方米="m^2", 立方厘米="cm^3", 立方分米="dm^3", 立方毫米="mm^3",
    千克="kg", 克="g", 吨="t", 毫克="mg",
    秒="s", 毫秒="ms", 小时="h", 分钟="min",
    厘米每秒="cm/s", 米每秒="m/s", 千米每小时="km/h",
    度=r"^{\circ}", 摄氏度=r"^{\circ}C",
    千克每立方米="kg/m^3", 立方米每小时="m^3/h", 吨每分钟="t/min",
    帕斯卡="Pa", 帕="Pa", 千帕="kPa", 千帕斯卡="kPa",
    牛顿="N", 牛="N",
    安培="A", 安="A", 欧姆=r"\Omega", 欧=r"\Omega", 伏特="V", 伏="V",
)
NO_RM_CHINESE_UNIT = {"度", "摄氏度"}
CHINESE_UNIT_LIST = list(CHINESE_UNIT_TO_LATEX_MAPPER.keys())


def check_json_file(file):
    """ checkk is given file is a `json` extension file """
    return file.endswith('.json')


def trans_chinese_unit_to_latex(sent: str) -> str:
    preceding_slash = False
    in_formula = False

    valid_group_list = []
    for idx, char in enumerate(sent):
        if char == "\\":
            preceding_slash = True
        elif char == "$":
            if preceding_slash:
                # $ preceding with \ is not a valid sign of start or end of latex
                preceding_slash = False
                continue
            else:
                in_formula = not in_formula

            if not in_formula:
                valid_start_idx = idx + 1
                while valid_start_idx + 1 < len(sent) and sent[valid_start_idx+1] == " ":
                    valid_start_idx += 1

                chinese_unit = _starts_with_chinese_unit(sent[valid_start_idx:])
                if chinese_unit is not None:
                    valid_group_list.append(
                        [idx, valid_start_idx + len(chinese_unit), chinese_unit]
                    )
        else:
            preceding_slash = False

    out_seg_list = []
    start_idx = 0
    for group in valid_group_list:
        if group[2] in NO_RM_CHINESE_UNIT:
            seg = "{} {}$".format(
                sent[start_idx: group[0]], CHINESE_UNIT_TO_LATEX_MAPPER[group[2]]
            )
        else:
            seg = "{} \\rm {}$".format(
                sent[start_idx: group[0]], CHINESE_UNIT_TO_LATEX_MAPPER[group[2]]
            )

        start_idx = group[1]
        out_seg_list.append(seg)

    out_seg_list.append(sent[start_idx:])

    return "".join(out_seg_list)


def _starts_with_chinese_unit(sent: str) -> bool:
    global CHINESE_UNIT_LIST
    for unit in CHINESE_UNIT_LIST:
        if sent.startswith(unit):
            return unit

    return None


def split_to_latex_and_not(sent: str):
    start_idx, seg_list = 0, []
    preceding_slash, in_formula = False, False

    for idx, char in enumerate(sent):
        if char == "\\":
            preceding_slash = True
        elif char == "$":
            if preceding_slash:
                preceding_slash = False
                continue

            in_formula = not in_formula
            if in_formula:
                seg_list.append(sent[start_idx: idx])
                start_idx = idx
            else:
                seg_list.append(sent[start_idx + 1: idx])
                start_idx = idx + 1
        else:
            preceding_slash = False

    seg_list.append(sent[start_idx:])

    return seg_list

