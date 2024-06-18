from typing import Any
class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arguments(metaclass=SingletonMeta):
    def __init__(self):
        self.current_param_lists = None
        self.buffered_param_lists = []
        self.param_lists_of_loops = None
        self.current_dept = 0
        self.max_dept = 0

    def get_upcoming_arguments(self, caller_name: str) -> dict[str, Any] | None:
        ret_val = None
        while self.current_param_lists and (not ret_val or caller_name not in ret_val):
            ret_val = self.current_param_lists.pop(0)
        if caller_name in ret_val:
            if ret_val[caller_name] and type(ret_val[caller_name]) is list:
                return ret_val[caller_name][0]
            else:
                return None
        else:
            return None

    def replace_current_argument_lists(self):
        self.buffered_param_lists.append(self.current_param_lists)
        self.current_param_lists = self.param_lists_of_loops[self.current_dept].copy()
        self.current_dept += 1
        if self.current_dept > self.max_dept:
            self.max_dept = self.current_dept

    def renew_loop_argument_lists(self):
        self.current_param_lists = self.param_lists_of_loops[self.current_dept-1].copy()

    def restore_last_buffered_argument_list(self):
        self.current_param_lists = self.buffered_param_lists.pop()
        self.current_dept -= 1
        if self.current_dept == 0:
            del self.param_lists_of_loops[:self.max_dept]
            self.max_dept = 0
