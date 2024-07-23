# Copyright (c) 2024 Snowflake Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import pytest
from pygls.lsp.client import BaseLanguageClient
from lsprotocol import types
import pytest_asyncio
from snowflake.connector import SnowflakeConnection

from snowflake.cli.plugins.lsp.utils import ConnectionParams

START_ARGS = ["snow", "lsp", "start"]


@pytest_asyncio.fixture
async def lsp_client():
    """
    Return a client configured to communicate with a server running under cpython.
    """

    client = BaseLanguageClient("snowcli-lsp-test-suite", "v1")
    await client.start_io(*START_ARGS)

    response = await client.initialize_async(
        types.InitializeParams(
            capabilities=types.ClientCapabilities(),
        )
    )
    assert response is not None

    yield client

    await client.shutdown_async(None)
    client.exit(None)

    await client.stop()


@pytest.fixture
def lsp_connection_params(snowflake_session: SnowflakeConnection) -> ConnectionParams:

    # Grab the connection! And the tokens are on the connection.rest object. Alarmingly which might get removed in the future?
    # maybe we should save the master/session on the connection object itself rather than in SnowflakeRestful.
    connection = snowflake_session
    if not connection.rest._token:
        pytest.exit("Cannot continue without session token")

    if not connection.rest._master_token:
        pytest.exit("Cannot continue without master token")

    return ConnectionParams(
        session_token=connection.rest._token,
        master_token=connection.rest._master_token,
        account=connection.account,
        connection_name="",  # FIXME: what is this?
        params={},
    )


@pytest.mark.asyncio
@pytest.mark.integration_experimental
async def test_lsp_client_and_server(
    lsp_client: BaseLanguageClient,
    lsp_connection_params,
):
    assert asyncio.get_running_loop()

    PROJECT_PATH = ".."  # TODO: use a test project directory

    params: ConnectionParams = {
        **lsp_connection_params,
        "params": {
            "project_path": PROJECT_PATH,
        },
    }

    response = await lsp_client.workspace_execute_command_async(
        types.ExecuteCommandParams("bundleApplication", [params])
    )
    assert response["_message"] == "https://..."  # TODO: valid URL
