import os
from remote_get_update import RemoteGetUpdateData
import static_code
import logs_init_code
import structure_depend_code as sd

class MoveFilesAddJupyterLinks(RemoteGetUpdateData):
    """
public Interface methods:
    move_files_add_jupyter_links

if something goes wrong and
you need all methods use this code:
for method in dir(Interface):
    print(method)
    """


    @classmethod
    @static_code.check_file_path_exist
    @static_code.break_and_return_if_none_arg
    def move_file_to_vm(cls, path=None, full_path_destination_file=None):
        """Move file to vm dir"""
        #full_path_source_file = sd.get_full_path_obj_stor_files(file_name)
        #full_path_destination_file = sd.get_full_path_current_hw_files(file_name)

        #os.system(f'mv {full_path_source_file} {full_path_destination_file}
        full_path_source_file = path
        os.system(f'cp {full_path_source_file} {full_path_destination_file}')


    @classmethod
    @static_code.break_and_raise_exception_if_none_arg
    @static_code.log_start_end_function_name
    def processing_local_data_jupyter_links(cls, stream_mipt, all_hw_to_save):
        # if all_hw_to_save empty return {}, []

        by_title_column_name_get_index_of_update_list = {}

        #logs_init_code.backend_logger.debug(str(all_hw_to_save.items()))
        files_to_move = []
        column_name = "jupyter link"

        list_of_update_list = []
        index_of_update_list = 0

        for title, list_of_by_column_name_get_value in all_hw_to_save.items():
            static_code.append_or_update_if_exist_nested_dict(by_title_column_name_get_index_of_update_list, [title, column_name], index_of_update_list)
            list_of_update_list.append([])
            for index in range(sd.first_student_jndex - 2, len(list_of_by_column_name_get_value)):
                current_row = list_of_by_column_name_get_value[index]
                is_latest = current_row['latest']
                student_file_name = current_row['file name']
                jupyter_link = current_row['jupyter link']
                if is_latest == 'TRUE':
                    generated_link = sd.generate_jupyter_link(student_file_name)
                    puted = generated_link

                    files_to_move.append(student_file_name)
                    source_path = sd.get_full_path_obj_stor_files(stream_mipt, title, student_file_name)
                    destination_path = sd.get_full_path_current_hw_files(student_file_name)
                    if jupyter_link == '':
                        cls.move_file_to_vm(path=source_path,
                                            full_path_destination_file=destination_path)

                        logs_init_code.backend_logger.debug(f"move {source_path}, ' -> ', {destination_path}")
                    else:
                        logs_init_code.backend_logger.debug(f"jupyter_link not empty => was moved to {destination_path}")


                else:
                    puted = jupyter_link


                list_of_update_list[index_of_update_list].append(puted)
                logs_init_code.backend_logger.debug(f"\n{jupyter_link}\n {student_file_name}, 'is_latest:', {is_latest}, '-> puted: ', {puted}")

            index_of_update_list += 1


        return by_title_column_name_get_index_of_update_list, list_of_update_list, files_to_move


    @static_code.break_and_return_if_none_arg
    #@static_code.catch_interrupting_exception
    @static_code.log_start_end_function_name
    def move_files_add_jupyter_links(self, stream_mipt, hw_list):
        """
        Moves files and adds jupyter links for a given stream and homework list.
        Args:
            stream_mipt (str): by stream_mipt in json get link to remote table
            hw_list (list): List of homework items to process.
        Returns: None
        """
        all_hw_to_save, by_hw_column_name_get_index = self.download_remote_table(stream_mipt, hw_list)
        by_title_column_name_get_index_of_update_list, list_of_update_list, files_to_move = self.processing_local_data_jupyter_links(stream_mipt, all_hw_to_save)
        logs_init_code.backend_logger.debug(str(files_to_move))
        #self.move_all_files_to_vm(files_to_move)
        self.update_remote_table(stream_mipt, by_title_column_name_get_index_of_update_list, list_of_update_list, by_hw_column_name_get_index)
        if static_code.is_no_exeptions:
            print("DONE")
        else:
            print("BAD; CHECK LOGS: THERE WHERE A COUPLE OF EXCEPTIONS")
