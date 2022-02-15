import json
import logging

from websocket import WebSocket, create_connection

HASS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiIxNzI0YmI3MTY2NzU0MDdiYmIzODY0ODNjNTJiYzdiOSIsImlhdCI6MTY0NDE1MTAyNSwiZXhwIjoxOTU5NTExMDI1fQ.0Qv5YJy5UuMWU9Win5273P0JurWSK3ZoyO1LhNNwzX8"
LOGGER = logging.getLogger("TEST_WEBSOCKET_FIXTURE")


def runSocketCommandAndReceiveReturn(command_type: str, parameters: dict = None):
    wc = create_connection("ws://localhost:8123/api/websocket")
    if authenticate(wc):

        command = {"type": command_type, "id": 1}
        if parameters != None:
            command.update(parameters)

        LOGGER.debug("Will send")
        LOGGER.debug(stringifymsg(command))
        wc.send(stringifymsg(command))
        result = dignifymsg(wc.recv())
    wc.close()

    if "result" in result:
        return result
    else:
        LOGGER.error(result)
        return False


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
