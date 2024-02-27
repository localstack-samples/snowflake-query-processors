# LocalStack Snowflake Query Processors

Sample repo for adding new query processors to the LocalStack Snowflake emulator.

## Prerequisites

* Python 3.10+
* Docker
* LocalStack Pro account, with Snowflake extension enabled

## Installing

Run the following command to install the dependencies for this repo:
```
$ make install
```

## Building and Running

For all commands below, make sure to have your `LOCALSTACK_AUTH_TOKEN` configured in your terminal session.

Run this command to build the extension in this repo:
```
$ make build
```

Run this command to install the extension into the LocalStack environment:
```
$ make enable
```

Run the following command to start up LocalStack Snowflake:
```
$ IMAGE_NAME=localstack/snowflake SF_LOG=trace DEBUG=1 localstack start
```

If the installation was successful, you should be able to `curl` the session endpoint:
```
$ curl -d '{}' snowflake.localhost.localstack.cloud:4566/session
{"success": true}
```

## Testing

Use this target to trigger the integration tests, which will run a couple of simple commands/queries against the local Snowflake emulator:
```
$ make test
```

To iterate on the tests: Whenever you make some changes to the plugin logic, make sure to run `make build; make enable`, and then restart your LocalStack container to fully re-load the code in a new session. Once restarted, the tests can be executed again via `make test`.

## License

The code in this repo is published under the Apache 2.0 license.
