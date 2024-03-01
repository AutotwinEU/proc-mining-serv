import logging
from flask import Flask, json, Response
from paste.translogger import TransLogger

LOG_FORMAT = "%(asctime)s %(message)s"
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
MSG_FORMAT = (
    "%(REMOTE_ADDR)s - %(REMOTE_USER)s "
    '"%(REQUEST_METHOD)s %(REQUEST_URI)s %(HTTP_VERSION)s" '
    '%(status)s %(bytes)s "%(HTTP_REFERER)s" "%(HTTP_USER_AGENT)s"'
)

logging.basicConfig(format=LOG_FORMAT, datefmt=DATE_FORMAT, level=logging.INFO)
app = Flask("proc-mining-serv")
wsgi = TransLogger(app, format=MSG_FORMAT, setup_console_handler=False)


@app.post("/graph-model")
def create_graph_model() -> Response:
    """
    Create a graph model in the SKG.
    """
    response_data = json.dumps({"model_id": 0})
    return Response(response_data, status=201, mimetype="application/json")


@app.post("/petri-net")
def create_petri_net() -> Response:
    """
    Create a Petri net in the SKG.
    """
    response_data = json.dumps({"model_id": 0})
    return Response(response_data, status=201, mimetype="application/json")


@app.post("/automaton")
def create_automaton() -> Response:
    """
    Create an automaton in the SKG.
    """
    response_data = json.dumps({"model_id": 0})
    return Response(response_data, status=201, mimetype="application/json")


if __name__ == "__main__":
    import waitress

    waitress.serve(wsgi, host="localhost")
