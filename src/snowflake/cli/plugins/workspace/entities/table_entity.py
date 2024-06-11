from __future__ import annotations

from snowflake.cli.plugins.workspace.entities.entity_base import Entity


class TableEntity(Entity):
    def __init__(self, entity_config):
        super().__init__(entity_config)

    def create_deploy_plan_impl(self, ctx, plan, *args, **kwargs):
        db_name = ctx.get_db_name()
        schema_name = ctx.get_schema_name()
        table_name = self.config["name"]
        columns = self.config["columns"]
        plan.add_sql(
            f"CREATE TABLE IF NOT EXISTS {db_name}.{schema_name}.{table_name} ({columns[0]});"
        )
