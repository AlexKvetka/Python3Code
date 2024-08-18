import random
import os

import logs_init_code
import send_function_code
import static_code
import structure_depend_code as sd

"""
Exist naming:
index (vertical move like in matrix)
and jndex (horizontal move like in matrix)
"""


class RemoteGetUpdateData:
    """An ideologically private: Class for managing remote updates and data retrieval."""
    by_stream_mipt_get_table_link = sd.links_from_json  # .read()

    @classmethod
    @static_code.break_and_raise_exception_if_none_arg
    def full_authorization(cls, stream_mipt):
        """Full authorization to Google table."""
        gc = sd.authorize_gc()
        table_link = cls.by_stream_mipt_get_table_link.get(f"{stream_mipt}_assignee_table_link", None)
        if table_link is None:
            static_code.is_no_exeptions = False
            raise Exception

        sh = gc.open_by_url(table_link)
        logs_init_code.backend_logger.debug(str(sh.worksheets()))

        return sh.worksheets()

    @staticmethod
    @static_code.break_and_return_if_none_arg
    def update_column(ws, letter, start_num, new_column_list):
        """Update remote column by list."""
        length_new_column_list = len(new_column_list)
        formatted_list = [[new_column_list[i]] for i in range(length_new_column_list)]
        end_num = start_num + length_new_column_list
        logs_init_code.backend_logger.debug(str([letter, start_num, end_num, length_new_column_list]))
        ws.update(range_name=f'{letter}{start_num}:{letter}{end_num}', values=formatted_list)

    @classmethod
    @static_code.break_and_raise_exception_if_none_arg
    @static_code.log_start_end_function_name
    def update_remote_table(cls, stream_mipt, by_title_column_name_get_index_of_update_list, list_of_update_list,
                            by_hw_column_name_get_index):
        """Update Jupyter link remote table by stream mipt and new values."""
        by_title_get_ws = static_code.get_nested_dict_value(cls.by_stream_mipt_and_title_get_ws, [stream_mipt])
        for title, by_column_name_get_index_of_update_list in by_title_column_name_get_index_of_update_list.items():
            iter_ws = static_code.get_nested_dict_value(by_title_get_ws, [title])
            if iter_ws is None:
                static_code.is_no_exeptions = False
                logs_init_code.backend_logger.debug(
                    f"NOT FOUND WS: {title} IN LOCAL STREAM MIPT TABLE; CONTINUE UPDATE OTHER")
                continue

            for column_name, index_of_update_list in by_column_name_get_index_of_update_list.items():
                jndex = by_hw_column_name_get_index[title][column_name]
                cls.update_column(iter_ws, static_code.get_column_letter(jndex + 1), sd.first_student_jndex,
                                  list_of_update_list[index_of_update_list])

            for column_name, index_of_update_list in by_column_name_get_index_of_update_list.items():
                jndex = by_hw_column_name_get_index[title][column_name]
                logs_init_code.backend_logger.debug(f"{column_name}")
                for i in range(len(list_of_update_list[index_of_update_list])):
                    logs_init_code.backend_logger.debug(f"{sd.first_student_jndex + i} {list_of_update_list[index_of_update_list][i]}")


    @classmethod
    @static_code.break_and_raise_exception_if_none_arg
    @static_code.log_start_end_function_name
    def download_remote_table(cls, stream_mipt, hw_list=None):
        """Download remote table to local data.csv file."""
        hw_set = set(hw_list) if hw_list else set()
        work_sheets_list = cls.full_authorization(stream_mipt)
        if not work_sheets_list:
            return {}, {}

        cls.by_stream_mipt_and_title_get_ws = {}
        for ws in work_sheets_list:
            static_code.append_or_update_if_exist_nested_dict(cls.by_stream_mipt_and_title_get_ws, [stream_mipt,
                                                                                                    ws.title], ws)

        hw_ws = []
        if not hw_list:
            by_title_get_ws = static_code.get_nested_dict_value(cls.by_stream_mipt_and_title_get_ws, [stream_mipt])
            if by_title_get_ws:
                hw_ws = [ws for title, ws in by_title_get_ws.items() if sd.title_hw_contains_criteria in title]
        else:
            by_title_get_ws = static_code.get_nested_dict_value(cls.by_stream_mipt_and_title_get_ws, [stream_mipt])
            if by_title_get_ws:
                hw_ws = []
                for title, ws in by_title_get_ws.items():
                    if sd.title_hw_contains_criteria in title and title in hw_set:
                        hw_ws.append(ws)
                        hw_set.remove(title)


        if hw_set:
            static_code.is_no_exeptions = False
            static_code.log_and_print(f"NOT FOUND IN {stream_mipt}, SUCH HOMEWORKS {hw_set}, OTHER HOMEWORKS WILL BE PROCESSED")

        all_hw_to_save = {}
        by_hw_column_name_get_index = {}
        logs_init_code.backend_logger.debug(str(hw_ws))
        for ws in hw_ws:
            hw = ws.title
            list_of_dicts = ws.get_all_records()
            row_with_column_name = ws.get_all_values()[0]

            by_hw_column_name_get_index[hw] = dict(zip(row_with_column_name, range(len(row_with_column_name))))
            all_hw_to_save[hw] = list_of_dicts

            #logs_init_code.backend_logger.debug(list_of_dicts)

        return all_hw_to_save, by_hw_column_name_get_index

    @staticmethod
    def normal_shuffle(x):
        """Shuffle the list and return as a string."""
        random.shuffle(x)
        x = ''.join(x)
        return x

    @classmethod
    def filling(cls):
        """Fill method."""
        stream_mipt = '2023s'
        work_sheets_list = cls.full_authorization(stream_mipt)
        ws = work_sheets_list[1]
        num = 100
        logs_init_code.backend_logger.debug(str((ws, num)))

        # usual = ['' for i in range(num)]
        # usual = ['kashtelian.mv@phystech.edu', ...
        # cls.update_column(ws, "Q", 3, usual)
        # cls.update_column(ws, "M", 3, usual)
        # cls.update_column(ws, "J", 3, usual)
        # cls.update_column(ws, "P", 3, usual)
        # cls.update_column(ws, "K", 3, usual)
        # cls.update_column(ws, "O", 3, usual)
        # logs_init_code.backend_logger.debug(' '.join(usual))
        # cls.update_column(ws, "C", 3, usual)
