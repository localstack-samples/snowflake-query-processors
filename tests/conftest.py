import pytest
import snowflake.connector

pytest_plugins = [
    "localstack_snapshot.pytest.snapshot",
]


@pytest.fixture
def snowflake_connection_params():
    return {
        "user": "test",
        "password": "test",
        "account": "test",
        "database": "test",
        "host": "snowflake.localhost.localstack.cloud",
    }


@pytest.fixture
def snowflake_connection(snowflake_connection_params):
    connection = snowflake.connector.connect(**snowflake_connection_params)

    connection.cursor().execute("USE DATABASE test")
    connection.cursor().execute("USE SCHEMA public")

    yield connection

    connection.close()


@pytest.fixture
def db_execute(snowflake_connection):
    def _execute(*args, **kwargs):
        result = snowflake_connection.cursor().execute(*args, **kwargs)
        return list(result)

    return _execute
