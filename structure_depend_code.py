import logging
import os
import sys
import gspread as gs
import logs_init_code
import send_function_code
import static_code
sys.path.insert(1, '/home/pracstats/stats-course/configs')
from configs import configs

# Set the environment variable for the stats directory
path_to_course = os.environ['STATS_DIR']

# Set logging mode
logging_mode = logging.DEBUG
logs_init_code.backend_logger.setLevel(logging_mode)
logs_init_code.ch.setLevel(logging_mode)

# Set path to authorization file
autorize_file_path = os.path.join(path_to_course, 'configs/google_service_account.json')

# Constants
first_student_jndex = 3
title_hw_contains_criteria = 'hw'


def generate_jupyter_link(file_name):
    return os.path.join('http://localhost:8888/notebooks/current-hw-files/', file_name)


# Email login credentials and message
login_email = 0#
login_password = 0#
subject = 'Практикум по статистике'
text = 'Спасибо за домашнее задание.'

# Function to send file


@static_code.check_file_path_exist
def send_file(send_to='', path=''):
    send_function_code.send_mail(login_email, login_password, send_to, subject, text, path)

# Paths for files


def get_full_path_obj_stor_files(stream_mipt, hw, file_name):
    return os.path.join(path_to_course, f'obj-stor/{stream_mipt}/{hw}/submitted/{file_name}')


def get_full_path_current_hw_files(file_name):
    return os.path.join(path_to_course, f'current-hw-files/{file_name}')


# Initialize Google Sheets client
authorize_client = static_code.ReadWriteJson(autorize_file_path)


def authorize_gc():
    return gs.service_account_from_dict(authorize_client.read())


# Load links from configuration file
links_from_json = configs

