import re
from typing import Tuple

from .stream import Stream, check_stream_idx_valid
from ..mapping.token_mapping import (
    normalize_token, lower_token, is_left_marker, is_right_marker,
    is_angle_marker, normalize_sentence_char
)

class LatexTokenStream(Stream):
    """ Latex string tokenizer """
    invalid_char = {
        ' '
    }
    complete_token_mapper = {
        "sin": "\\sin", 
        "cos": "\\cos", 
        "tan": "\\tan", 
        "lg": "\\lg", 
        "ln": "\\ln", 
        "log": "\\log",
    }
    
    continue_alpha = re.compile(r"^\\[A-Za-z]+")
    continue_alpha_num = re.compile(r"^\\[A-Za-z0-9]+")
    discrete_alpha_num = re.compile(r"^( )+[A-Za-z0-9]+( )+[A-Za-z0-9]+")
    double_slash = re.compile(r"^\\\\")

    def __init__(self, 
                 latex_str: str, 
                 normalize_token=None, 
                 ignore_similar_despite_capital: bool = False,
                 keep_left_right_marker: bool = True,
                 strip_angle: bool = False):

        self._stream = latex_str
        self._current_idx = 0
        self._peek_delta_idx = 0

        self._normalize_token = normalize_token
        self.ignore_similar_despite_capital = ignore_similar_despite_capital
        self.keep_left_right_marker = keep_left_right_marker
        self.strip_angle = strip_angle

        if self._normalize_token:
            self._stream = normalize_sentence_char(self._stream)

    @check_stream_idx_valid
    def read(self):
        token = self.peek()
        self._current_idx += self._peek_delta_idx
        return token

    @check_stream_idx_valid
    def read_frag(self):
        token = self.peek_frag()
        self._current_idx += self._peek_delta_idx
        return token

    @check_stream_idx_valid
    def peek(self):
        token = self._peek_one_token()
        while token is not None and not self.is_valid_token(token):
            self._read_one_token()
            token = self._peek_one_token()

        return token

    @check_stream_idx_valid
    def peek_frag(self):
        token = self._peek_one_frag_token()
        while token is not None and not self.is_valid_token(token):
            self._read_one_token()
            token = self._peek_one_frag_token()

        return token

    def _read_one_token(self):
        token = self._peek_one_token()
        self._current_idx += self._peek_delta_idx
        return token

    def _peek_one_token(self):
        next_token, peek_delta_idx = (
            self._get_token(self._stream[self._current_idx:])
        )
        
        next_token, self._peek_delta_idx = (
            self.further_tokenize(next_token, peek_delta_idx)
        )

        if next_token == '':
            return None
        else:
            if self._normalize_token:
                next_token = normalize_token(next_token)
            if self.ignore_similar_despite_capital:
                next_token = lower_token(next_token)
            return next_token

    def _peek_one_frag_token(self):
        next_token, peek_delta_idx = (
            self._get_frag_token(self._stream[self._current_idx:])
        )
        
        next_token, self._peek_delta_idx = (
            self.further_tokenize(next_token, peek_delta_idx)
        )

        if next_token == '':
            return None
        else:
            if self._normalize_token:
                next_token = normalize_token(next_token)
            if self.ignore_similar_despite_capital:
                next_token = lower_token(next_token)
            return next_token

    @check_stream_idx_valid
    def read_with_re(self, pattern):
        token = self.peek_with_re(pattern)
        if token is None:
            return None

        self._current_idx += self._peek_delta_idx
        return token

    @check_stream_idx_valid
    def peek_with_re(self, pattern):
        if isinstance(pattern, str):
            pattern = re.compile(pattern)

        char, delta_idx = self._read_until_valid()
        if char is None:
            return None
        self._peek_delta_idx = delta_idx
        # self._current_idx += delta_idx

        result = pattern.match(self._stream[self._current_idx+delta_idx:])

        if result is None:
            return None

        token, self._peek_delta_idx = (
            self.further_tokenize(result.group(), delta_idx + len(result.group()))
        )

        if pattern.match(token) is None:
            return None
        else:
            return token

    @check_stream_idx_valid
    def peek_one_char(self):
        char, delta_idx = self._peek_one_char()
        self._peek_delta_idx = delta_idx

        return char

    def _peek_one_char(self):
        delta_idx = 0
        char = None
        for idx, _char in enumerate(self._stream[self._current_idx:]):
            delta_idx = idx + 1
            if _char not in self.invalid_char:
                char = _char
                break

        return char, delta_idx

    @check_stream_idx_valid
    def read_one_char(self):
        char = self.peek_one_char()
        self._current_idx += self._peek_delta_idx

        return char

    def _read_until_valid(self):
        for idx, char in enumerate(self._stream[self._current_idx:]):
            if char not in self.invalid_char:
                return char, idx

        return None, None

    def get_all_tokens(self):
        tokens = []
        token = self.read()
        while token is not None:
            tokens.append(token)
            token = self.read()
        
        return tokens

    def tokenize(self):
        tokens = []
        token = self.read_frag()
        while token is not None:
            tokens.append(token)
            token = self.read_frag()
        
        return tokens

    def is_valid_token(self, token: str):
        if not self.keep_left_right_marker:
            if is_left_marker(token) or is_right_marker(token):
                return False

        if self.strip_angle:
            if is_angle_marker(token):
                return False
        
        return True

    def further_tokenize(self, token: str, delta_idx: int) -> Tuple[str, int]:
        """ seperated sinx -> \sin x """
        if not self.is_token_to_further_tokenize(token):
            return token, delta_idx

        len_token = len(token)
        for test_token, target_token in self.complete_token_mapper.items():
            if test_token not in token:
                continue

            # corner case, arcsine, arccos, arctan should not be seperated
            if test_token in {"sin", "cos", "tan"} and "arc"+test_token in token:
                continue

            search_result = self.match_with_inserted_empty_space(
                test_token, 
                self._stream[self._current_idx: self._current_idx+delta_idx]
            )
            test_idx = token.index(test_token)
            if test_idx == -1:
                continue
            elif test_idx > 0:
                return token[:test_idx], search_result.span()[0]
            elif test_idx == 0:
                return target_token, search_result.span()[1]

        return token, delta_idx

    def is_token_to_further_tokenize(self, token: str) -> bool:
        return re.match("[ a-zA-Z0-9]+", token) is not None

    def match_with_inserted_empty_space(self, pattern: str, token: str): 
        pattern = "\s*".join(list(pattern))
        return re.search(pattern, token)

    # ================== Data Accessor ========================
    def get_stream_str(self):
        return self._stream

    # ================== Status Controller ==========================
    def reset_stream(self):
        self._current_idx = 0
        self._peek_delta_idx = 0

    def enable_strip_angle(self):
        self.strip_angle = True

    def disable_strip_angle(self):
        self.strip_angle = False

    def _get_frag_token(self, input_str: str):
        if input_str == '':
            return '', 0

        start_idx, end_idx = 0, 0
        for idx, char in enumerate(input_str):
            if char in self.invalid_char:
                continue

            start_idx, end_idx = idx, idx
            if char == '\\':
                alpha_idx = self._read_continue_alpha(input_str[start_idx:])
                slash_idx = self._read_slash(input_str[start_idx:])
                one_sign_idx = 2
                end_idx = max(alpha_idx, slash_idx, one_sign_idx) + start_idx

            elif char.isnumeric():
                end_idx = self._read_num(input_str[start_idx:]) + start_idx
                
            elif char.isalpha() and char.isupper():
                end_idx = self._read_upper_alpha(input_str[start_idx:]) + start_idx
                
            else:
                end_idx += 1

            break

        return input_str[start_idx:end_idx].replace(' ', ''), end_idx

    def _get_token(self, input_str: str):
        if input_str == '':
            return '', 0

        start_idx, end_idx = 0, 0
        for idx, char in enumerate(input_str):
            if char in self.invalid_char:
                continue

            start_idx, end_idx = idx, idx
            if char == '\\':
                alpha_idx = self._read_continue_alpha(input_str[start_idx:])
                slash_idx = self._read_slash(input_str[start_idx:])
                one_sign_idx = 2
                end_idx = max(alpha_idx, slash_idx, one_sign_idx) + start_idx
                
            elif char.isalnum():
                end_idx = self._read_alpha_num(input_str[start_idx:]) + start_idx
                
            else:
                end_idx += 1

            break

        return input_str[start_idx:end_idx].replace(' ', ''), end_idx

    def _read_continue_alpha(self, input_str: str):
        match_result = self.continue_alpha.search(input_str)
        if match_result is None:
            return 0
        else:
            return match_result.span()[1]

    def _read_alpha(self, input_str: str):
        return_idx = -1
        for idx, char in enumerate(input_str):
            if char in self.invalid_char:
                continue

            if char.isalpha():
                return_idx = idx
            else:
                break

        return return_idx + 1

    def _read_alpha_num(self, input_str: str):
        return_idx = -1
        for idx, char in enumerate(input_str):
            if char in self.invalid_char:
                continue

            if char.isalnum() or char == '.':
                return_idx = idx
            else:
                break

        return return_idx + 1

    def _read_slash(self, input_str: str):
        match_result = self.double_slash.search(input_str)
        if match_result is None:
            return 0
        else:
            return match_result.span()[1]

    def _read_upper_alpha(self, input_str: str):
        return_idx = -1
        for idx, char in enumerate(input_str):
            if char in self.invalid_char:
                continue

            if char.isalpha() and char.isupper():
                return_idx = idx
            else:
                break

        return return_idx + 1

    def _read_num(self, input_str: str):
        return_idx = -1
        for idx, char in enumerate(input_str):
            if char in self.invalid_char:
                continue

            if char.isnumeric() or char == ".":
                return_idx = idx
            else:
                break

        return return_idx + 1
