import requests


def web_session(session_args: requests.Request) -> requests.Response:
    """Requests an arbitrary remote resource using the provided `Request`-formatted object.

    :param sessionArgs : Requests-formatted session arguments.
    """

    session = requests.Session()
    prepared_request = session.prepare_request(session_args)
    response: requests.Response = session.send(prepared_request)

    return response
