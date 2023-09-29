import json
import os
from pathlib import Path

import strictyaml
from snowcli.cli.common.sql_execution import SqlExecutionMixin
from snowflake.connector.cursor import SnowflakeCursor


class ServiceManager(SqlExecutionMixin):
    def create(
        self,
        service_name: str,
        compute_pool: str,
        spec_path: Path,
        num_instances: int,
    ) -> SnowflakeCursor:
        spec = self._read_yaml(spec_path)
        return self._execute_schema_query(
            f"""\
            CREATE SERVICE IF NOT EXISTS {service_name}
            IN COMPUTE POOL {compute_pool}
            FROM SPECIFICATION '
            {spec}
            '
            WITH
            MIN_INSTANCES = {num_instances}
            MAX_INSTANCES = {num_instances}
            """
        )

    def _read_yaml(self, path: Path) -> str:
        # TODO(aivanou): Add validation towards schema
        with open(path, "r") as content:
            spec_obj = strictyaml.load(content)
            return json.dumps(spec_obj)

    def desc(self, service_name: str) -> SnowflakeCursor:
        return self._execute_schema_query(f"desc service {service_name}")

    def show(self) -> SnowflakeCursor:
        return self._execute_schema_query("show services")

    def status(self, service_name: str) -> SnowflakeCursor:
        return self._execute_schema_query(
            f"CALL SYSTEM$GET_SERVICE_STATUS('{service_name}')"
        )

    def drop(self, service_name: str) -> SnowflakeCursor:
        return self._execute_schema_query(f"drop service {service_name}")

    def logs(self, service_name: str, container_name: str):
        return self._execute_schema_query(
            f"call SYSTEM$GET_SERVICE_LOGS('{service_name}', '0', '{container_name}');"
        )
