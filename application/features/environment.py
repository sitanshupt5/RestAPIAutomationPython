import os
import sys

from commons.config.logging_config import get_logger
from commons.utils.file_handlers import FileHandlers

Logger = get_logger("HooksLogger")

before_hook_executed = False
performance_map = {}
performance_scenario_map = {}
total_scenario = 1
tags_passed = None


def before_all(context):
    global before_hook_executed
    global tags_passed
    file_handler = FileHandlers()
    if not before_hook_executed:
        for i, arg in enumerate(sys.argv):
            if '--tags' in arg:
                tags_passed = sys.argv[i].split('=')[1]
                break

        if tags_passed is None:
            tags_passed = os.environ.get("tags")

            # Directory to be deleted
            report_directory_to_delete = "./allure-report"

            # Check if the directory exists\
            file_handler.delete_file_or_directory(report_directory_to_delete)

            results_directory_to_delete = "./allure-results"
            # Check if the directory exists
            file_handler.delete_file_or_directory(results_directory_to_delete)

            before_hook_executed = True


def after_all(context):
    # Capture relevant environment information
    env = context.config.userdata.get('env')
    if env is None:
        env = os.environ.get("env")
    env_info = {
        'Environment': os.getenv('Environment', env),
        'Python version': os.sys.version,
        'Project': os.getcwd()
    }
    with open('./allure-results/environment.properties', 'w') as f:
        for key, value in env_info.items():
            f.write(f"{key}={value}\n")
