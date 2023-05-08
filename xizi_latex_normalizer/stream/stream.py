import functools


class Stream(object):
    invalid_char = set()

    def read(self):
        """ Read and return a token and forward the stream """
        raise NotImplementedError

    def peek(self):
        """ Read and return a token and not forward the stream """
        raise NotImplementedError

def check_stream_idx_valid(func):
    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        if self._current_idx >= len(self._stream):
            return None
        else:
            return func(self, *args, **kwargs)

    return wrap
