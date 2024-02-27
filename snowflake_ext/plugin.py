from abc import ABC

from snowflake_local.engine.models import Query
from snowflake_local.engine.query_processors import QueryProcessor as _QueryProcessor
from snowflake_local.server.models import QueryResponse
from sqlglot import exp


class QueryProcessor(ABC):
    """
    Base class for query processors, which provide an extension point to add custom
    query processing logic. Each query processor can define either a query transformation,
    or a query result postprocessor, or a combination of both.
    Additionally, query processors can define custom extension functions directly in
    the underlying Postgres DB engine.
    """

    def initialize_db_resources(self, database: str):
        """
        Initialize and create the required resources (e.g., functions) against the given database.

        The following utility method can be used to execute queries against the underlying Postgres DB:
            snowflake_local.engine.postgres.db_state.State.Server.run_query(query: str, database: str)
        """

    def should_apply(self, query: Query) -> bool:
        """Whether to apply this processor to the given query."""
        return True

    def transform_query(self, expression: exp.Expression, query: Query) -> exp.Expression:
        """Preprocess the given query fragment, apply any required transformations, return the result."""
        return expression

    def postprocess_result(self, query: Query, result: QueryResponse):
        """Postprocess the given query and modify the result, as required."""

    def get_priority(self) -> int:
        """
        Return priority of this processor, to enable a simple dependency mechanism
        between different transformers that depend on each other.

        Higher returned number means higher priority, i.e., processors with higher
        priority number are executed prior to processors with lower numbers. Execution
        order of processors with the same priority number is indeterministic.
        """
        return 0


# ---
# Query processor plugin implementation below ...
# ---


class ProcessHelloWorldQueries(_QueryProcessor):

    def transform_query(self, expression: exp.Expression, **kwargs) -> exp.Expression:
        from sqlglot import parse_one  # noqa

        # TODO: add query transformation logic here...
        # Note: to transform the incoming query to return a static query response, the
        # `sqlglot.parse_one` utility function can be used, for example:
        #       return sqlglot.parse_one("SELECT 'string to return ...'")

        return expression
