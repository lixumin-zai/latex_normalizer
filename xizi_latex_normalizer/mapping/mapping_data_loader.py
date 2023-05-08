import json
import os

from ..utils.common_utils import check_json_file


DIR_PATH = os.path.dirname(os.path.abspath(__file__))


class DataReaderSingleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = (
                super(DataReaderSingleton, cls).__new__(cls, *args, *kwargs)
            )
        return cls._instance

    def __init__(self):
        self._init = True

    @classmethod
    def relase(cls):
        cls._instance = None


class TokenMappingDataReader(DataReaderSingleton):
    """ Class for reading data for mapping token
    
    Attributes:
        _data(dict): mapping dict for token mapping
        data_path(str): file path where `_data` from
    """
    def __init__(self, data_path=None):
        if hasattr(self, "_init"):
            return

        super().__init__()

        self.data_path = (
            data_path or os.path.join(DIR_PATH, "mapping_data", "mapping_dict.json")
        )
        self._data = self.read(self.data_path)

    def get_normalized_token(self, token: str):
        if self._data is None:
            raise ValueError("No valid data provided for token mapping")
        
        return self._data.get(token, token)

    def read(self, data_path):
        """ Read json file as token mapping """
        if not check_json_file(data_path):
            raise ValueError("The file for token mapping data must be json")

        with open(data_path, "r", encoding="utf-8") as rfile:
            return json.load(rfile)


class TokenIgnoringCaptalMappingDataReader(DataReaderSingleton):
    """ Class for reading data of token mapping with similar form of capital
    and lower case
    
    Attributes:
        _data(dict): mapping dict for token mapping
        data_path(str): file path where `_data` from
    """
    def __init__(self, data_path=None):
        if hasattr(self, "_init"):
            return

        super().__init__()

        self.data_path = (
            data_path or os.path.join(DIR_PATH, 
                                      "mapping_data", 
                                      "similar_cap_token_dict.json")
        )
        self._data = self.read(self.data_path)

    def get_lower_case_token(self, token: str):
        if self._data is None:
            raise ValueError("No valid data provided for token mapping")
        
        return self._data.get(token, token)

    def read(self, data_path):
        """ Read json file as token mapping """
        if not check_json_file(data_path):
            raise ValueError("The file for token mapping data must be json")

        with open(data_path, "r", encoding="utf-8") as rfile:
            return json.load(rfile)


class GlobalCharMappingDataReader(DataReaderSingleton):
    """ Class for reading data of token mapping with similar form of capital
    and lower case
    
    Attributes:
        _data(dict): mapping dict for token mapping
        data_path(str): file path where `_data` from
    """
    def __init__(self, data_path=None):
        if hasattr(self, "_init"):
            return

        super().__init__()

        self.data_path = (
            data_path or os.path.join(DIR_PATH, 
                                      "mapping_data", 
                                      "global_char_mapping.json")
        )
        self._data = self.read(self.data_path)

    def get_all_chars(self):
        return list(self._data.keys())

    def get_mapped_char(self, char: str):
        if self._data is None:
            raise ValueError("No valid data provided for token mapping")
        
        return self._data.get(char, char)

    def read(self, data_path):
        """ Read json file as token mapping """
        if not check_json_file(data_path):
            raise ValueError("The file for token mapping data must be json")

        with open(data_path, "r", encoding="utf-8") as rfile:
            return json.load(rfile)




