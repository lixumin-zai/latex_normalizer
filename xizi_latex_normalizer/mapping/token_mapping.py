import os
import re

from .mapping_data_loader import (
    TokenMappingDataReader, TokenIgnoringCaptalMappingDataReader,
    GlobalCharMappingDataReader
)


def normalize_token(token: str):
    """ Normalize token if equal expression recorded, return `token` elsewise """
    return TokenMappingDataReader().get_normalized_token(token)


def lower_token(token: str):
    """ Normalize token if it is similar token recorded, return `token` elsewise """
    return TokenIgnoringCaptalMappingDataReader().get_lower_case_token(token)


def normalize_sentence_char(sent: str):
    reader = GlobalCharMappingDataReader()
    for char in reader.get_all_chars():
        sent = re.sub(
            ("%r" % char).strip("'"), 
            ("%r" % reader.get_mapped_char(char)).strip("'"), 
            sent
        )

    return sent


def is_left_marker(token: str):
    return token == "\\left"


def is_right_marker(token: str):
    return token == "\\right"


def is_angle_marker(token: str):
    return token == "\\angle"
