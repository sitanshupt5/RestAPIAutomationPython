import os
import sys
import subprocess
from behave.__main__ import main as behave_main


def run_tests(tags=None, cur_dir=None, cur_env=None):
    args = [
        '-f', 'allure_behave.formatter:AllureFormatter',
        '-o', 'allure-results',
        '--no-capture',
        f'{cur_dir}/features'
    ]
    if tags:
        args.append(f'--tags={tags}')
        os.environ["tags"] = tags
    if cur_dir:
        os.environ["dir"] = cur_dir
    if cur_env:
        os.environ["env"] = cur_env
    return behave_main(args)


def generate_allure_report():
    allure_command = "allure generate allure-results/ --clean -o allure-report/"
    subprocess.run(allure_command, shell=True, check=True)


if __name__ == "__main__":
    exit_code = run_tests(tags="Smoke", cur_dir="application", cur_env="dev")
    generate_allure_report()
    sys.exit(exit_code)