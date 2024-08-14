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

from __future__ import annotations

from typing import List, Optional

from pydantic import Field
from snowflake.cli.api.project.schemas.references import NativeAppReference
from snowflake.cli.api.project.schemas.updatable_model import (
    IdentifierField,
    UpdatableModel,
)


class SqlScriptHookType(UpdatableModel):
    sql_script: str = Field(title="SQL file path relative to the project root")


# Currently sql_script is the only supported hook type. Change to a Union once other hook types are added
PostDeployHook = SqlScriptHookType


class Application(UpdatableModel):
    role: Optional[str] = Field(
        title="Role to use when creating the application object and consumer-side objects",
        description=f"""If you do not specify a role, Snowflake CLI attempts to use the default role assigned to your
        user in your Snowflake account. Typically, you specify this value in the snowflake.local.yml as described in
        {NativeAppReference.PROJECT_DEFINITION_OVERRIDES.value.get_link_text()}.
        """,
        default=None,
    )
    name: Optional[str] = Field(
        title="Name of the application object created when you run the snow app run command",
        description=f"""Based on your platform, Snowflake CLI uses the $USER, $USERNAME, or $LOGNAME environment
        variables. As with native_app.name, both unquoted and quoted identifiers are supported.
        Typically, you specify this value in the snowflake.local.yml as described in
        {NativeAppReference.PROJECT_DEFINITION_OVERRIDES.value.get_link_text()}.
        """,
        default=None,
    )
    warehouse: Optional[str] = IdentifierField(
        title="Name of the application object created when you run the snow app run command",
        description=f"""If you do not specify a warehouse, Snowflake CLI attempts to use the default warehouse assigned
        to your user in your Snowflake account.. Typically, you specify this value in the snowflake.local.yml as
        described in {NativeAppReference.PROJECT_DEFINITION_OVERRIDES.value.get_link_text()}.
    """,
        default=None,
    )
    debug: Optional[bool] = Field(
        title="When set, forces debug_mode on/off for the deployed application object",
        default=None,
    )
    post_deploy: Optional[List[PostDeployHook]] = Field(
        title="Actions that will be executed after the application object is created/upgraded",
        default=None,
    )


class ApplicationV11(Application):
    # Templated defaults only supported in v1.1+
    name: Optional[str] = Field(
        title="Name of the application object created when you run the snow app run command",
        default="<% fn.id_concat(ctx.native_app.name, '_', fn.clean_id(fn.get_username('unknown_user'))) %>",
    )
