def test_query_hello_world(db_execute):
    # first, try to run a simple SELECT query that should always work
    result = db_execute("SELECT 123")
    assert result == [(123,)]

    # second, try to select from a `hello_world` relation - the logic for this
    # needs to be implemented in the `ProcessHelloWorldQueries` class!
    result = db_execute("SELECT * FROM hello_world")
    assert result == [("Hello LocalStack Snowflake!",)]


def test_query_regexp_count_function(db_execute):
    # Test basic regex pattern matching
    result = db_execute("SELECT REGEXP_COUNT('hello world hello', 'hello')")
    assert result == [(2,)]

    # Test with case sensitive pattern
    result = db_execute("SELECT REGEXP_COUNT('Hello World HELLO', 'hello')")
    assert result == [(0,)]

    # Test with case insensitive flag
    result = db_execute("SELECT REGEXP_COUNT('Hello World HELLO', 'hello', 1, 'i')")
    assert result == [(3,)]

    # Test with position parameter
    result = db_execute("SELECT REGEXP_COUNT('hello world hello', 'hello', 7)")
    assert result == [(1,)]

    # Test with no matches
    result = db_execute("SELECT REGEXP_COUNT('hello world', 'goodbye')")
    assert result == [(0,)]

    # Test with empty string
    result = db_execute("SELECT REGEXP_COUNT('', 'hello')")
    assert result == [(0,)]

    # Test with NULL values (should handle gracefully)
    result = db_execute("SELECT REGEXP_COUNT(NULL, 'hello')")
    assert result == [(None,)]
