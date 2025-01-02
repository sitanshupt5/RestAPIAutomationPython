from behave import when
from commons.service_manager.response_manager import ResponseManager
from commons.config.logging_config import get_logger

logger = get_logger("WhenTestSteps")


@when('I call method "{request_type}"')
def i_call_method(context, request_type):
    resp = ResponseManager()
    resp.do_request_call(context, request_type)