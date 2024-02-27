from localstack.extensions.api import Extension


class SnowflakeHelloWorld(Extension):

    name = "snowflake-hello-world"

    def on_platform_start(self):
        # simply importing the query processor here, it will be
        # automatically discovered at runtime...
        from snowflake_ext import plugin  # noqa
