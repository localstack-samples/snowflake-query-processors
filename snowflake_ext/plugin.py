from abc import ABC

from localstack.pro.snowflake.engine.models import Query
from localstack.pro.snowflake.engine.query_processors import QueryProcessor as _QueryProcessor
from localstack.pro.snowflake.server.models import QueryResponse
from sqlglot import exp


class QueryProcessor(ABC):
    """
    Base class for query processors, which provide an extension point to add custom
    query processing logic. Each query processor can define either a query transformation,
    or a query result postprocessor, or a combination of both.
    Additionally, query processors can define custom extension functions directly in
    the underlying Postgres DB engine.
    """

    def initialize_db_resources(self) -> str | None:
        """
        Initialize and create the required resources (e.g., functions) against a newly created database.

        This method can return a string of SQL queries (separated by ';') to execute against the DB.
        """

    def should_apply(self, query: Query) -> bool:
        """Whether to apply this processor to the given query."""
        return True

    def transform_query(self, expression: exp.Expression, query: Query) -> exp.Expression:
        """
        Preprocess the given query fragment, apply any required transformations, return the result.

        Note that this method gets called on the initial user-defined query after we've parsed it
        via `sqlglot`. This method is called recursively for all query fragments (tree nodes)
        in the abstract syntax tree of the query, as outlined here:
        https://github.com/tobymao/sqlglot/blob/7b2cff84f9a544435aa22954536eb7c9c2632816/README.md?plain=1#L276-L294
        """
        return expression

    def postprocess_result(self, query: Query, result: QueryResponse):
        """Postprocess the given query and modify the result, as required."""

    def get_priority(self) -> int:
        """
        Return priority of this processor, to enable a simple dependency mechanism
        between different transformers that depend on each other.

        Higher returned number means higher priority, i.e., processors with higher
        priority number are executed prior to processors with lower numbers. Execution
        order of processors with the same priority number is non-deterministic.
        """
        return 0


# ---
# Query processor plugin implementation below ...
# ---


class HandleHelloWorldQueries(_QueryProcessor):

    def transform_query(self, expression: exp.Expression, **kwargs) -> exp.Expression:
        from sqlglot import parse_one  # noqa

        # TODO: add query transformation logic here...
        # Note: to transform the incoming query to return a static query response, the
        # `sqlglot.parse_one` utility function can be used, for example:
        #       return sqlglot.parse_one("SELECT 'string to return ...'")

        return expression


class HandleRegexpCountFunction(_QueryProcessor):
    """
    Query processor to enable the REGEXP_COUNT(..) Snowflake SQL function:
    https://docs.snowflake.com/en/sql-reference/functions/regexp_count
    """

    def initialize_db_resources(self) -> str | None:
        from localstack.pro.snowflake.engine.transforms import apply_query_transforms

        # TODO: Use this method to return the definition of a custom SQL function
        #  that implements `REGEXP_COUNT()` in the given database.
        # The following function languages are available and installed: SQL, plpython3u, javascript

        init_query = """
        ...
        """

        init_query = apply_query_transforms(init_query).query
        return init_query
