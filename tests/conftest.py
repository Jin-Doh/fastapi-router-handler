import logging

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastapi_router_handler import ExceptionHandler


@pytest.fixture
def logger():
    return logging.getLogger("test_logger")


@pytest.fixture
def exception_handler(logger):
    return ExceptionHandler(logger=logger)


@pytest.fixture
def app():
    return FastAPI()


@pytest.fixture
def client(app):
    return TestClient(app)
