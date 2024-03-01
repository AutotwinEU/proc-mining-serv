import pytest
import autotwin_pmswsgi as pms
from flask import Flask
from flask.testing import FlaskClient
from flask.testing import FlaskCliRunner


@pytest.fixture()
def app() -> Flask:
    """
    Define the test application.

    Yields:
        Test application.
    """
    pms.app.config.update({"TESTING": True})
    yield pms.app


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    """
    Define the test client.

    Args:
        app: Test application.

    Returns:
        Test client.
    """
    return app.test_client()


@pytest.fixture()
def runner(app: Flask) -> FlaskCliRunner:
    """
    Define the test CLI runner.

    Args:
        app: Test application.

    Returns:
        Test CLI runner.
    """
    return app.test_cli_runner()
