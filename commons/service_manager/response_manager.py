import base64
import json

import allure
import requests

from commons.config.logging_config import get_logger


class ResponseManager(object):
    """
    Class containing methods to execute api requests, capture responses and store response for further use.
    """

    def __init__(self):
        """
        Constructor for ResponseManager class. Used to initialise the logger for the class.
        """
        self.logger = get_logger("ResponseManager")
        self.logger.info("ResponseManager")

    def do_request_call(self, context, request_type):
        """
        Carries out operations ranging between:
        • Analysing, mapping, generating runtime data for request.
        • Executing the request.
        • Analysing and verifying response status.
        • Extracting and storing the response body.
        :param context: context object associated with the current cucumber scenario being executed.
        :param request_type: refers to the CRUD operations (GET, POST, PUT, DELETE, PATCH etc.).
        """
        session = requests.Session()
        attach_str = "Request Sent ::\n"
        attach_str = attach_str + str(request_type) + "Url :=" + str(context.url) + '\n'
        if hasattr(context, "access_token"):
            headers = context.header
            headers["Authorization"] = "Bearer " + context.access_token
        elif context.api == 'oauth2_token':
            encoded_cred = base64.b64encode(f"{context.client_id}:{context.client_secret}".encode()).decode()
            headers = context.header
            headers["Authorization"] = f"Basic {encoded_cred}"
        else:
            headers = context.header

        session.headers.update(headers)
        attach_str = attach_str + "Headers :=\n" + str(json.dumps(headers, indent=4)) + "\n"

        if hasattr(context, "username") and hasattr(context, "password"):
            username = context.username
            password = context.password
            session.auth = (username, password)
            attach_str = attach_str + "Username :=" + username + "\n" + "Password :=" + password + "\n"

        if hasattr(context, "query_params") and context.query_params is not None:
            q = context.query_params
            params_string = '&'.join([f"{key}={value}" for key, value in q.items()])
            if ':' in params_string:
                session.params = params_string
            else:
                session.params = context.query_params
                attach_str = attach_str + "Query_Params :=\n" + str(json.dumps(context.query_params, indent=4)) + '\n'

        if hasattr(context, "body") and context.body is not None:
            attach_str = attach_str + "Body :=" + str(json.dumps(context.body, indent=4)) + "\n"
            if request_type == "POST":
                if context.api == "oauth2_token":
                    response = session.post(context.url, data=context.body)
                else:
                    response = session.post(context.url, json=context.body)
            elif request_type == "GET":
                response = session.get(context.url, json=context.body)
            elif request_type == "PUT":
                response = session.put(context.url, json=context.body)
            elif request_type == "DELETE":
                response = session.delete(context.url, json=context.body)
        else:
            if request_type == "POST":
                response = session.post(context.url)
            elif request_type == "GET":
                response = session.get(context.url)
            elif request_type == "DELETE":
                response = session.delete(context.url)

        context.status_code = response.status_code
        context.time_taken = response.elapsed.total_seconds() * 1000
        attach_str = attach_str + "\n\nResponse :" + "\n" + "status_code :=" + str(response.status_code)
        context.response = response.json()
        attach_str = attach_str + "\n" + str(json.dumps(response.json(), indent=4))
        allure.attach(attach_str, name="API Response", attachment_type=allure.attachment_type.TEXT)
        self.logger.info(f"Response is ::: \n{json.dumps(context.response, indent=4)}")
