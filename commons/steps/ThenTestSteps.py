from behave import then
from commons.config.logging_config import get_logger
from commons.service_manager.assertion_manager import AssertionManager

logger = get_logger("ThenTestSteps")


@then('I save the access token')
def i_save_the_access_token(context):
    context.access_token = context.response['access_token']
    logger.info("Access token saved.")


@then('I verify response code is  "{statuscode}"')
def i_verify_response_code(context, statuscode):
    assertion = AssertionManager()
    assertion.assert_response_code(context, statuscode)


@then('I verify attribute values match "{validation_data}" in response')
def i_verify_attribute_value_match(context, validation_data):
    assertion = AssertionManager()
    assertion.validate_response_values(context, validation_data)