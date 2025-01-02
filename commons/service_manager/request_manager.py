import json
import os
import yaml
import pandas as pd

from commons.config.logging_config import get_logger


class RequestManager:
    """
    Class containing methods to initialise and construct appropriate requests associated with api's.
    """

    def __init__(self):
        """
        Constructor for the RequestManager class. Used to initialise the logger for the class.
        """
        self.logger = get_logger("RequestManager")
        self.logger.info("Request Manager")

    def set_all_files_path(self, run_dir, env, context):
        """
        Method set the filepaths for request.json, testdata.yml and validation_mapping.yml files
        associated with an api's request.
        :param run_dir: relative file of the application project for which the api request is to be sent.
        :param env: relative path of the directory which stores data specific to the environment for which
                    the api request is to be executed.
        :param context: context object associated with the current cucumber scenario being executed.
        """
        context.request_path = os.path.abspath(
            os.path.join(os.getcwd(), run_dir, "apischema", env, context.api, 'request.json'))
        context.testdata_path = os.path.abspath(
            os.path.join(os.getcwd(), run_dir, "apischema", env, context.api, "testdata.yml"))
        context.validation_path = os.path.abspath(
            os.path.join(os.getcwd(), run_dir, "apischema", env, context.api, "validation_mapping.yml"))

    def get_env_dir(self, context):
        """
        fetches details of application project path whose scenarios are to be executed along with the environment
        path from where the execution data for the scenario is to be found.
        :param context: context object associated with the current cucumber scenario being executed.
        """
        run_dir = context.config.userdata.get('dir')
        env = context.config.userdata.get('env')
        if run_dir is None:
            run_dir = os.environ.get("dir")
        if env is None:
            env = os.environ.get("env")
        context.env = env
        return run_dir, env

    def set_paths(self, context):
        """
        fetches relative paths of the application project as well as the path for the scenario data environment
        and sets the absolute paths.
        :param context: context object associated with the current cucumber scenario being executed.
        """
        (run_dir, env) = self.get_env_dir(context)
        self.set_all_files_path(run_dir, env, context)

    def set_testdata(self, context):
        """
        Fetches path of testdata.yml file from the scenario context and uses it to fetch the appropriate
        dataset associated with the current executing scenario and then store it the scenario context.
        :param context: context object associated with the current cucumber scenario being executed.
        """
        with open(context.testdata_path, "r") as file:
            context.test_data = yaml.safe_load(file)[context.dataset]

    def set_config_path(self, context):
        """
        Fetches path of the envconfig.yml file of the application project whose feature file is currently
        being executed. Then fetches all parameter values from the file for the current environment and
        stores the individual parameter values to the context.
        :param context: context object associated with the current cucumber scenario being executed.
        """
        (run_dir, env) = self.get_env_dir(context)
        context.envconfig_path = os.path.abspath(
            os.path.join(os.getcwd(), run_dir, "config", "envconfig.yml"))
        context.env = env
        with open(context.envconfig_path, "r") as file:
            context.config_dataset = yaml.safe_load(file)[context.env]
            context.client_id = context.config_dataset["clientId"]
            context.client_secret = context.config_dataset["clientSecret"]

    def set_api_parameters(self, context):
        """
        Extracts all available data regarding the api request schema eg.(uri, body, headers, authentication
        params, query params etc.) and stores then in the scenario context.
        :param context: context object associated with the current cucumber scenario being executed.
        """
        self.set_paths(context)
        self.set_config_path(context)
        with open(context.envconfig_path, "r") as file:
            if context.api == "oauth2_token":
                url = yaml.safe_load(file)[context.env]['token_uri']
            else:
                url = yaml.safe_load(file)[context.env]['host_uri']
            self.logger.info(url)
        path_to_file = context.request_path
        with open(path_to_file, "r", encoding="utf-8") as file:
            data = json.load(file)
            self.logger.info(f"Data is : {data}")
            base_path = data["base_path"]
            context.url = url + base_path
            if "query_params" in data:
                context.query_params = data["query_params"]
            if "auth_params" in data:
                context.username = data["auth_params"]["username"]
                context.password = data["auth_params"]["password"]
            if "header" in data:
                context.header = data["header"]
            if "request" in data:
                context.body = data["request"]

    def delete_existing_context_attributes(self, context):
        """
        Deletes parameters and values stored in scenario context associated. This is especially necessary in
        case of scenarios that involve orchestration with more than 1 api request. The method removes data
        of request schema that belongs to the previous api for it to be rewritten for the current api.
        :param context: context object associated with the current cucumber scenario being executed.
        """
        if hasattr(context, "api"):
            del context.api
        if hasattr(context, "query_params"):
            del context.query_params
        if hasattr(context, "username"):
            del context.username
        if hasattr(context, "password"):
            del context.password
        if hasattr(context, "header"):
            del context.header
        if hasattr(context, "body"):
            del context.body

    def set_request_body(self, context, dataset):
        """
        Fetches request body, query params associated with an api and replaces the parameterized for actual
        values present in the dataset of the currently executing scenario.
        :param context: context object associated with the current cucumber scenario being executed.
        :param dataset: execution data associated with the currently executing scenario.
        """
        path_to_file = context.testdata_path
        with open(path_to_file, "r") as file:
            data_dict = yaml.safe_load(file)
            data = data_dict[dataset]
            df = pd.DataFrame(data_dict)
            context.expected_df = pd.DataFrame(df[dataset])
            if hasattr(context, "body") and context.body is not None:
                payload = context.body
                body = self.process_json(payload, data)
                self.logger.info(f"Body is :{body}")
                context.body = body
            if hasattr(context, "query_params") and context.query_params is not None:
                query_param = self.process_json(context.query_params, data)
                self.logger.info(f"query param is : {query_param}")
                context.query_params = query_param

    def process_json(self, json_data, replace_map):
        """
        Fetches a json schema with parameterized values and maps the placeholders for the parameters with
        actual values from the replace_map.
        :param json_data: the json body schema with parameterized values.
        :param replace_map: mapping for parameters and actual values.
        """
        if isinstance(json_data, list):
            new_list = []
            for item in json_data:
                if isinstance(item, str) and item.startswith('(') and item.endswith(')'):
                    param_name = item[1:-1]
                    if param_name in replace_map:
                        new_list.append(replace_map[param_name])
                else:
                    result = self.process_json(item, replace_map)
                    if result:
                        new_list.append(result)
            return new_list if new_list else None
        elif isinstance(json_data, dict):
            new_dict = {}
            for key, value in list(json_data.items()):
                if isinstance(value, str) and value.startswith('(') and value.endswith(')'):
                    param_name = value[1:-1]
                    if param_name in replace_map:
                        new_dict[key] = replace_map[param_name]
                    elif isinstance(value, (list, dict)):
                        result = self.process_json(value, replace_map)
                        if result:
                            new_dict[key] = result
            return new_dict if new_dict else None

