from flask.testing import FlaskClient


def test_create_graph_model(client: FlaskClient):
    """Test the creation of a graph model.

    Args:
        client: Test client.
    """
    response = client.post("/graph-model")
    assert response.status_code == 201


def test_create_petri_net(client: FlaskClient):
    """Test the creation of a Petri net.

    Args:
        client: Test client.
    """
    response = client.post("/petri-net")
    assert response.status_code == 201


def test_create_automaton(client: FlaskClient):
    """
    Test the creation of an automaton.

    Args:
        client: Test client.
    """
    c_type = "application/json"

    payload = """{
    "test": "true",
    "pov": "plant",
    "start": "0",
    "end": "1000"
    }"""
    response = client.post("/automaton", data=payload, content_type=c_type)
    assert response.status == "201 CREATED"

    payload = """{
    "pov": "plant",
    "end": "1000"
    }"""
    response = client.post("/automaton", data=payload, content_type=c_type)
    assert response.status == "400 BAD REQUEST"
