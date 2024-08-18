from remote_get_update import RemoteGetUpdateData
import static_code
import logs_init_code
import structure_depend_code as sd

"""
Exist naming:
index(vertical move like in matrix) 
and jndex(horizontal move like in matrix)
 """

class SendCheckedFiles(RemoteGetUpdateData):
    """
public Interface methods:
    send_checked_files

if something goes wrong and
you need all methods use this code:
for method in dir(Interface):
    print(method)
    """

    @classmethod
    @static_code.break_and_raise_exception_if_none_arg
    @static_code.log_start_end_function_name
    def processing_local_data_files_to_send(cls, all_hw_to_save, assignee_list=[]):
        criterias_column_name = ['is checked', 'is sent']
        criteria_funcs = [lambda x: x == "TRUE", lambda x: x == "FALSE"]
        if assignee_list:
            assignee_set = set(assignee_list)
            criterias_column_name.append('assignee')
            criteria_funcs.append(lambda x: x in assignee_set)

        by_title_column_name_get_index_of_update_list = {}
        logs_init_code.backend_logger.debug(f"{criterias_column_name}")
        #logs_init_code.backend_logger.debug(str(all_hw_to_save.items()))
        files_to_move = []
        column_name = "is sent"

        list_of_update_list = []
        index_of_update_list = 0

        for title, list_of_by_column_name_get_value in all_hw_to_save.items():
            static_code.append_or_update_if_exist_nested_dict(by_title_column_name_get_index_of_update_list, [title, column_name],
                                                  index_of_update_list)
            list_of_update_list.append([])
            for index in range(sd.first_student_jndex - 2, len(list_of_by_column_name_get_value)):

                current_row = list_of_by_column_name_get_value[index]
                logs_init_code.backend_logger.debug(f"\n{current_row}")
                current_criteria_values = list(map(lambda x: current_row[x], criterias_column_name))
                is_criteria = True
                for i in range(len(current_criteria_values)):
                    logs_init_code.backend_logger.debug(
                        f"{criterias_column_name[i]} {criteria_funcs[i](current_criteria_values[i])}")
                    if not criteria_funcs[i](current_criteria_values[i]):
                        is_criteria = False
                        logs_init_code.backend_logger.debug(f'-> {is_criteria}')
                        break
                    logs_init_code.backend_logger.debug(f'-> {is_criteria}')

                if is_criteria:
                    send_to = current_row['email']

                    att_path = sd.get_full_path_current_hw_files(current_row['file name'])
                    sd.send_file(path=att_path, send_to=send_to)
                    logs_init_code.backend_logger.debug(f"SEND: {send_to}  FILE: {att_path}")
                    puted = True
                    list_of_update_list[index_of_update_list].append(puted)
                else:
                    puted = current_row['is sent'] == 'TRUE'
                    list_of_update_list[index_of_update_list].append(puted)


                logs_init_code.backend_logger.debug(f"STUDENT: {current_row['email']} PUTED:{puted}")

            index_of_update_list += 1

        # for title, by_column_name_get_index_update_list in by_title_column_name_get_index_of_update_list.items():
        #     for column_name, index_update_list in by_column_name_get_index_update_list.items():
        #         new_list = '\n'.join(list(map(lambda x: str(x),
        #                                       list(enumerate(list_of_update_list[index_update_list],
        #                                                      start=sd.first_student_jndex)))))
        #         logs_init_code.backend_logger.debug(f"{title}: \n{new_list}\n")

        #logs_init_code.backend_logger.debug('\n'.join(files_to_move))

        return by_title_column_name_get_index_of_update_list, list_of_update_list

    @static_code.break_and_return_if_none_arg
    #@static_code.catch_interrupting_exception
    @static_code.log_start_end_function_name
    def send_checked_files(self, stream_mipt, hw_list=[], assignee_list=[]):
        """
    Sends checked files to students.
    Args:
        stream_mipt (str): by stream_mipt in json get link to remote table .
        hw_list (list, optional): List of homework items to process. Defaults for all homeworks.
        assignee_list (list, optional): List of assignees. Defaults for all assignees.
    Returns: None
    """
        all_hw_to_save, by_hw_column_name_get_index = self.download_remote_table(stream_mipt, hw_list)
        by_title_column_name_get_index_of_update_list, list_of_update_list = self.processing_local_data_files_to_send(
            all_hw_to_save, assignee_list)

        self.update_remote_table(stream_mipt, by_title_column_name_get_index_of_update_list,
                                 list_of_update_list, by_hw_column_name_get_index)
        if static_code.is_no_exeptions:
            print("DONE")
        else:
            print("BAD; CHECK LOGS: THERE WHERE A COUPLE OF EXCEPTIONS")


