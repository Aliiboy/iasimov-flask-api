import unittest

from flask.testing import FlaskClient
from flask_openapi3.openapi import OpenAPI

from infra.data.sql_database import SQLDatabase
from infra.web.app import WebApp
from infra.web.container import AppContainer


class BaseAPITest(unittest.TestCase):
    web_application: OpenAPI
    client: FlaskClient
    database: SQLDatabase

    @classmethod
    def setUpClass(cls) -> None:
        container = AppContainer()
        container.init_resources()
        web_app_instance = WebApp(container=container)
        cls.web_application = web_app_instance.app
        cls.client = cls.web_application.test_client()
        cls.database = container.database()
        cls.database.create_database()

    def setUp(self) -> None:
        self.session_context = self.database.get_session()
        self.session = self.session_context.__enter__()

    def tearDown(self) -> None:
        self.session_context.__exit__(None, None, None)
