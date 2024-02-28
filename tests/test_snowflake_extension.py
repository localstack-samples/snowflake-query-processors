def test_query_hello_world(db_execute):
    # first, try to run a simple SELECT query that should always work
    result = db_execute("SELECT 123")
    assert result == [(123,)]

    # second, try to select from a `hello_world` relation - the logic for this
    # needs to be implemented in the `ProcessHelloWorldQueries` class!
    result = db_execute("SELECT * FROM hello_world")
    assert result == [("Hello LocalStack Snowflake!",)]


def test_query_endswith_function(db_execute):
    # positive test case
    result = db_execute("SELECT STARTSWITH('localstack-snowflake', 'localstack-')")
    assert result == [(True,)]

    # negative test case
    result = db_execute("SELECT STARTSWITH('localstack-snowflake', 'foobar-')")
    assert result == [(False,)]
