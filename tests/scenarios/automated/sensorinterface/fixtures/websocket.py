import json
import logging

from websocket import WebSocket, create_connection

HASS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJiY2NlMzEwNmNmNzc0NWJlYjRhYTMzOTYzMGI5ZDczOCIsImlhdCI6MTY0MTc0NDk1NiwiZXhwIjoxOTU3MTA0OTU2fQ.ZdqLaXDC4gnX8JKSKYKRD0j7jdrQP8eBkD8MnTHH1y8"
LOGGER = logging.getLogger("TEST_WEBSOCKET_FIXTURE")


def runSocketCommandAndReceiveReturn(command_type: str, parameters: dict = None):
    wc = create_connection("ws://localhost:8123/api/websocket")
    if authenticate(wc):

        command = {"type": command_type, "id": 1}
        if parameters != None:
            command.update(parameters)

        wc.send(stringifymsg(command))
        result = dignifymsg(wc.recv())
    wc.close()
    return result


def authenticate(wc: WebSocket):
    wc.recv()
    wc.send(stringifymsg({"type": "auth", "access_token": HASS_TOKEN}))
    result_raw = wc.recv()
    LOGGER.debug(f"received authentification result: {result_raw}")
    result = dignifymsg(result_raw)
    if result["type"] == "auth_ok":
        return True
    else:
        raise ResourceWarning()


def stringifymsg(obj: dict):
    return json.dumps(obj)


def dignifymsg(msg: str):
    return json.loads(msg)
