import logging
import os
from tempfile import TemporaryDirectory

import autotwin_gmglib as gmg
from flask import Flask, request, json, Response
from paste.translogger import TransLogger
from semantic_main.autotwin_mapper import write_semantic_links
from sha_learning.autotwin_learn import learn_automaton
from skg_main.autotwin_connector import delete_automaton, store_automaton
from werkzeug.exceptions import HTTPException

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

NEO4J_URI = os.environ["NEO4J_URI"]
NEO4J_USERNAME = os.environ["NEO4J_USERNAME"]
NEO4J_PASSWORD = os.environ["NEO4J_PASSWORD"]
NEO4J_DATABASE = os.environ["NEO4J_DATABASE"]


@app.post("/graph-model")
def create_graph_model() -> Response:
    """Create a graph model in the SKG.

    Returns:
        Response with model ID.
    """
    request_data = request.get_data()
    config = json.loads(request_data)
    work_directory = TemporaryDirectory()
    config["work_path"] = work_directory.name
    config["neo4j"]["uri"] = NEO4J_URI
    config["neo4j"]["username"] = NEO4J_USERNAME
    config["neo4j"]["password"] = NEO4J_PASSWORD
    config["neo4j"]["database"] = NEO4J_DATABASE
    config["data"]["path"] = "log.csv"
    config["model"]["path"] = "model.json"
    gmg.import_log(config)
    log = gmg.load_log(config)
    model = gmg.generate_model(log, config)
    model_id = gmg.export_model(model, config)
    response_data = json.dumps({"model_id": model_id})
    return Response(response_data, status=201, mimetype="application/json")


@app.post("/petri-net")
def create_petri_net() -> Response:
    """Create a Petri net in the SKG.

    Returns:
        Response with model ID.
    """
    response_data = json.dumps({"model_id": 0})
    return Response(response_data, status=201, mimetype="application/json")


@app.post("/automaton")
def create_automaton() -> Response:
    """
    Create an automaton in the SKG.
    """
    data = request.json
    mime_type = "application/json"

    try:
        pov = data["pov"].upper()
        start = int(data["start"])
        end = int(data["end"])

        # TODO: to be fixed with a proper testing approach.

        if "test" in data:
            scs_msg = """{{\"status\": \"{}\",
            \"learned_sha_name\": \"{}\",
            \"pov\": \"{}\",
            \"from\": \"{}\",
            \"to\": \"{}\"}}"""
            msg = scs_msg.format("OK", "TEST-0", pov, start, end)

            response = Response(msg, status=201, mimetype=mime_type)
            return response

        try:
            # 1: Automata Learning experiment.
            learned_sha = learn_automaton(pov, start_ts=start, end_ts=end)

            # 2: Delete learned automaton from the SKG,
            # if there already exists one with the same name.
            delete_automaton(learned_sha, pov, start, end)

            # 3: Store the learned automaton into the SKG.
            store_automaton(learned_sha, pov, start, end)

            # 4: Create semantic links between learned model
            # and existing SKG nodes.
            write_semantic_links(learned_sha, pov, start, end)

            scs_msg = """{{\"status\": \"{}\",
            \"learned_sha_name\": \"{}\",
            \"pov\": \"{}\",
            \"from\": \"{}\",
            \"to\": \"{}\"}}"""
            msg = scs_msg.format("OK", learned_sha, pov, start, end)

            response = Response(msg, status=201, mimetype=mime_type)

        except Exception:
            logging.exception("Error")

            error_msg = "An error occurred. Learning unsuccessful."
            scs_msg = """{{\"status\": \"{}\",
            \"error\": \"{}\"}}"""
            msg = scs_msg.format("KO", error_msg)

            response = Response(msg, status=500, mimetype=mime_type)

    except KeyError:
        error_msg = "Incorrectly formatted request."
        scs_msg = """{{\"status\": \"{}\",
        \"error\": \"{}\"}}"""
        msg = scs_msg.format("KO", error_msg)
        response = Response(msg, status=400, mimetype=mime_type)

    return response


@app.errorhandler(HTTPException)
def transform_exception(error) -> Response:
    """Transform an HTTP exception into the JSON format.

    Returns:
        Response with error information.
    """
    response = error.get_response()
    response.data = json.dumps(
        {
            "code": error.code,
            "name": error.name,
            "description": error.description,
        }
    )
    response.content_type = "application/json"
    return response


if __name__ == "__main__":
    import waitress

    waitress.serve(wsgi, host="localhost")
