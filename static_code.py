import json
import traceback
import gspread as gs
import os
from datetime import datetime
import logs_init_code
import pytz

is_no_exeptions = True

class ReadWriteJson:
    def __init__(self, file_name):
        self.file_name = file_name

    def write(self, write_dict):
        try:
            with open(self.file_name, 'w') as f:
                json.dump(write_dict, f)
        except Exception as e:
            globals()['is_no_exeptions'] = False
            logs_init_code.backend_logger.critical(e)
            raise Exception

    def read(self):
        try:
            with open(self.file_name, 'r') as f:
                read_dict = json.load(f)
        except Exception as e:
            globals()['is_no_exeptions'] = False
            logs_init_code.backend_logger.critical(e)
            read_dict = {}

        return read_dict


def break_and_raise_exception_if_none_arg(func):
    def is_none_raise_wrapper(*args, **kwargs):
        for arg in args:
            if arg is None:
                globals()['is_no_exeptions'] = False
                logs_init_code.backend_logger.critical(f"SOME ARGUMENT IS {arg}; STOP INTERFACE FUNCTION CAUSE")
                raise Exception()

        for name, kwarg in kwargs.items():
            if kwarg is None:
                globals()['is_no_exeptions'] = False
                logs_init_code.backend_logger.critical(f"VARIABLE {name} IS {kwarg}; STOP INTERFACE FUNCTION CAUSE")
                raise Exception()

        return func(*args, **kwargs)
    return is_none_raise_wrapper


def break_and_return_if_none_arg(func):
    def none_args_return_wrapper(*args, **kwargs):
        for arg in args:
            if arg is None:
                globals()['is_no_exeptions'] = False
                logs_init_code.backend_logger.critical(f"SOME ARGUMENT IS {arg}; STOP MECHANICAL FUNCTION")
                return

        for name, kwarg in kwargs.items():
            if kwarg is None:
                globals()['is_no_exeptions'] = False
                logs_init_code.backend_logger.critical(f"VARIABLE {name} IS {kwarg}; STOP MECHANICAL FUNCTION")
                return

        return func(*args, **kwargs)
    return none_args_return_wrapper


def catch_interrupting_exception(func):
    def catch_interrupting_exception_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            globals()['is_no_exeptions'] = False
            print("BAD; CHECK LOGS: THERE WHERE A COUPLE OF EXCEPTIONS")
            logs_init_code.backend_logger.critical(f"THE EXECUTION OF THE {func.__name__} {e}")
            traceback.print_exc()

    return catch_interrupting_exception_wrapper


def check_file_path_exist(func):
    def path_check_wrapper(*args, **kwargs):
        full_path_source_file = kwargs['path']
        if isinstance(full_path_source_file, str):
            if os.path.isfile(full_path_source_file):
                return func(*args, **kwargs)
            else:
                globals()['is_no_exeptions'] = False
                if os.path.isdir(full_path_source_file):
                    logs_init_code.backend_logger.debug(f"IT IS A DIRECTORY {full_path_source_file}; CONTINUE OTHER")
                elif os.path.exists(full_path_source_file):
                    logs_init_code.backend_logger.critical(
                        f"NOT A DIR AND NOT A FILE {full_path_source_file}; CONTINUE OTHER")
                else:
                    logs_init_code.backend_logger.critical(
                        f"FILE OR DIR NOT EXIST {full_path_source_file}; CONTINUE OTHER")
        else:
            globals()['is_no_exeptions'] = False
            logs_init_code.backend_logger.critical(
                f"PATH NOT STR TYPE {full_path_source_file}; CONTINUE OTHER")

    return path_check_wrapper


beauty_print = 5

def log_and_print(text: str):
    logs_init_code.backend_logger.critical(text)
    print(text)

def log_start_end_function_name(func):
    def logging_wrapper(*args, **kwargs):
        global beauty_print
        s = beauty_print * ' '
        logs_init_code.backend_logger.info(f"{s} START_ {func.__name__} {datetime.now(pytz.timezone('Europe/Moscow'))}")
        beauty_print += 5
        result = func(*args, **kwargs)
        beauty_print -= 5
        logs_init_code.backend_logger.info(f"{s} FINISH {func.__name__} {datetime.now(pytz.timezone('Europe/Moscow'))}")
        return result

    return logging_wrapper


def get_column_letter(column_index):
    """
    Returns the column letter corresponding to the given column index.
    For example, get_column_letter(1) returns 'A', get_column_letter(27) returns 'AA', etc.
    """
    if column_index <= 0:
        raise ValueError("Column index must be a positive integer")

    column_letter = ""
    while column_index > 0:
        column_index -= 1
        column_letter = chr(column_index % 26 + ord('A')) + column_letter
        column_index //= 26

    return column_letter


@break_and_return_if_none_arg
def append_or_update_if_exist_nested_dict(nested_dict, keys, value):
    """Update or append an element in a nested dictionary."""
    current_dict = nested_dict
    for key in keys[:-1]:
        current_dict = current_dict.setdefault(key, {})
    current_dict[keys[-1]] = value


@break_and_return_if_none_arg
def get_nested_dict_value(nested_dict, keys):
    """Function to get value from nested dict using list of keys."""
    if keys and isinstance(nested_dict, dict):
        key = keys.pop(0)
        return get_nested_dict_value(nested_dict.get(key, {}), keys)

    return nested_dict if not keys else None
