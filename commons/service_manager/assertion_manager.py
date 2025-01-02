import re
import numpy as np
import jsonpath_rw_ext as jp
import yaml
import pandas as pd
from commons.config.logging_config import get_logger


class AssertionManager:
    """
    Class contains methods that facilitate different assertions.
    """

    def __init__(self):
        """
        Constructor for the AssertionManager class. Used to initialise the logger for the class.
        """
        self.logger = get_logger("AssertionManager_Logger")
        self.logger.info("AssertionManager")

    def assert_response_code(self, context, statuscode):
        """
        Verifies that the statuscode received in the api response matches the expected status code.
        :param context: context object associated with the current cucumber scenario being executed.
        :param statuscode: expected status code of the api response.
        """
        assert context.status_code == int(statuscode), f"Expected: {statuscode}, but got: {context.status_code}"
        self.logger.info("Verified status code")

    def assert_values(self, actual_value, exp_value):
        """
        Verifies if the actual value matches exactly with the expected value.
        :param actual_value: actual value in the api response.
        :param exp_value: expected value.
        :return:
        """
        assert str(actual_value) == str(exp_value), f"Expected: {exp_value}, but got: {actual_value}"
        self.logger.info("Verified values")

    def item_contains_value(self, actual_response, expected_property_value, property_path):
        """
        Verifies if the actual value contains the expected value.
        :param actual_response: api response in which the actual property value can be found.
        :param expected_property_value: value which is expected to be contained in the actual property value
        :param property_path: json path to the actual property value in the api response.
        """
        if isinstance(expected_property_value, str) and ',' in expected_property_value:
            json_path_expr = jp.parse('$.' + property_path)
            actual_property_value = json_path_expr.find(actual_response)[0].value
            expected_list = expected_property_value.split(",")
            for item in expected_list:
                assert item.strip() in actual_property_value, f'Expected: {item},' \
                                                              f' but got: {actual_property_value}'
        else:
            json_path_expr = jp.parse('$.' + property_path)
            actual_property_value = json_path_expr.find(actual_response)[0].value
            assert str(expected_property_value) in str(actual_property_value), \
                f"Expected: {expected_property_value}, but got: {actual_property_value}"

    def item_matches_regex(self, actual_response, expected_property_value, property_path):
        """
        Verifies if the format or the pattern of the actual property value in api response matches with the
        regex patter in the expected property value.
        :param actual_response: api response in which the actual property value can be found.
        :param expected_property_value: regex pattern with which the actual property value is supposed to match.
        :param property_path: json path to the actual property value in the api response.
        """
        json_path_expr = jp.parse('$.' + property_path)
        actual_property_value = json_path_expr.find(actual_response)[0].value
        self.logger.info(f"actual_property_value: {actual_property_value}")
        if isinstance(actual_property_value, list):
            if ',' in expected_property_value:
                expected_regex_list = expected_property_value.split(",")
                for item in actual_property_value:
                    for i in range(len(expected_regex_list)):
                        match = re.match(expected_regex_list[i], str(item[i]))
                        assert match, f'Regular Exp: {expected_regex_list[i]} did not match: {str(item[i])}'
            else:
                match = re.match(expected_property_value, actual_property_value)
                assert match, f"Regular Exp : {expected_property_value} did not match : {actual_property_value}"

    def item_matches_value(self, actual_response, expected_property_value, property_path):
        """
        Verifies if the actual value exactly matches with the expected value.
        :param actual_response: api response in which the actual property value can be found.
        :param expected_property_value: value with which the actual property value is supposed to exactly match.
        :param property_path: json path to the actual property value in the api response.
        """
        json_path_expr = jp.parse('$.' + property_path)
        actual_property_value = json_path_expr.find(actual_response)[0].value
        self.logger.info(f"actual_property_value: {actual_property_value}")
        if isinstance(actual_property_value, list) and len(actual_property_value) == 1:
            actual_property_value = actual_property_value[0]
        if expected_property_value is not None:
            if isinstance(actual_property_value,
                          str) and "\r" in actual_property_value and "\n" in actual_property_value:
                actual_property_value = actual_property_value.replace("\r", "").replace("\n", "")
            assert str(expected_property_value) == str(actual_property_value), \
                f"Expected: {expected_property_value}, but got: {actual_property_value}"

    def validate_response_values(self, context, validation_data):
        """
        Fetches property values from response and verifies whether:
        •   it contains expected value.
        •   matches an expected pattern.
        •   is equal to a particular value.
        :param context: context object associated with the current cucumber scenario being executed.
        :param validation_data: mapping between property and path to the property value in api response.
        """
        path_to_file = context.validation_path
        with open(path_to_file, "r") as file:
            data = yaml.safe_load(file)
            df = pd.DataFrame(data)
            self.logger.info(f"Data is : {df}")
            validate_data = pd.DataFrame(df[validation_data])
            validate_data.replace(np.nan, None, inplace=True)
            validate_df = validate_data.dropna()
            expect_df = context.expected_df
            actual_response = context.response
            self.logger.info(f"Actual Response: {actual_response}")
            for index, row in validate_df.iterrows():
                expected_property_value = expect_df.loc[index][0]
                self.logger.info(f"expected_property_value : {expected_property_value}")
                property_path = row[0]
                if 'Contains' in index:
                    self.item_contains_value(actual_response, expected_property_value, property_path)
                elif 'Regex' in index:
                    self.item_matches_regex(actual_response, expected_property_value, property_path)
                else:
                    self.item_matches_value(actual_response, expected_property_value, property_path)
