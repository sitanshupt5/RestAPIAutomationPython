from behave import given
from commons.service_manager.request_manager import RequestManager
from commons.config.logging_config import get_logger

logger = get_logger("GivenTestSteps")


@given('I have api "{api}"')
def i_have_api(context, api):
    req = RequestManager()
    req.delete_existing_context_attributes(context)
    context.api = api
    req.set_api_parameters(context)


@given('I set request body for "{dataset}"')
def i_set_request_body(context, dataset):
    req = RequestManager()
    req.set_request_body(context, dataset)