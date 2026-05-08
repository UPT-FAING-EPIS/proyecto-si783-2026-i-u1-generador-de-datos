import time
from neo4j import GraphDatabase
from schemas.connection import ConnectionTest, SchemaAnalysis, TableSchema, ColumnInfo, ConnectionCreate
from connectors.base import BaseConnector
from datetime import datetime, timezone

class Neo4jConnector(BaseConnector):

    def _get_driver(self):
        uri = f"bolt://{self.config.host}:{self.config.port}"
        return GraphDatabase.driver(
            uri,
            auth=(self.config.username or "neo4j", self.password or "")
        )

    async def test_connection(self) -> ConnectionTest:
        try:
            t0 = time.time()
            driver = self._get_driver()
            with driver.session() as session:
                result = session.run("RETURN 1 as ping")
                result.single()
                ver_result = session.run("CALL dbms.components() YIELD versions RETURN versions[0] as v")
                version = ver_result.single()["v"]
            driver.close()
            return ConnectionTest(
                success=True,
                message="Conexion exitosa",
                engine_version=f"Neo4j {version}",
                latency_ms=round((time.time()-t0)*1000, 2)
            )
        except Exception as e:
            return ConnectionTest(success=False, message=str(e))

    async def analyze_schema(self) -> SchemaAnalysis:
        driver = self._get_driver()
        tables = []
        relationships_list = []
        try:
            with driver.session() as session:
                labels_result = session.run("CALL db.labels() YIELD label RETURN label")
                labels = [r["label"] for r in labels_result]

                for label in labels:
                    count_result = session.run(f"MATCH (n:`{label}`) RETURN count(n) as c")
                    row_count = count_result.single()["c"]

                    sample_result = session.run(f"MATCH (n:`{label}`) RETURN n LIMIT 20")
                    props: dict[str, set] = {}
                    for record in sample_result:
                        for k, v in record["n"].items():
                            dtype = type(v).__name__
                            if k not in props:
                                props[k] = set()
                            props[k].add(dtype)

                    columns = []
                    for pname, dtypes in props.items():
                        columns.append(ColumnInfo(
                            name=pname,
                            data_type=" | ".join(dtypes),
                            is_nullable=True,
                            is_primary_key=False,
                            is_unique=False,
                            is_foreign_key=False,
                        ))

                    tables.append(TableSchema(
                        name=label,
                        row_count=row_count,
                        columns=columns,
                    ))

                rel_result = session.run("CALL db.relationshipTypes() YIELD relationshipType RETURN relationshipType")
                for r in rel_result:
                    relationships_list.append({"type": r["relationshipType"]})

        finally:
            driver.close()

        return SchemaAnalysis(
            engine="neo4j",
            database=self.config.database_name or "neo4j",
            tables=tables,
            relationships=relationships_list,
            total_tables=len(tables),
            analyzed_at=datetime.now(timezone.utc),
        )

    def get_max_id(self, table: str, pk_col: str) -> int:
        return 0

    def get_existing_ids(self, table: str, pk_col: str) -> list:
        return []

    def get_existing_values(self, table: str, col: str) -> set:
        return set()

    async def execute_inserts(self, table: str, records: list[dict]) -> dict:
        if not records:
            return {"inserted": 0, "errors": []}
        driver = self._get_driver()
        inserted = 0
        errors = []
        try:
            with driver.session() as session:
                for i, record in enumerate(records):
                    try:
                        clean = {k: v for k, v in record.items() if v is not None and k != "_id"}
                        props = ", ".join([f"{k}: ${k}" for k in clean.keys()])
                        session.run(f"CREATE (n:`{table}` {{{props}}})", **clean)
                        inserted += 1
                    except Exception as e:
                        errors.append({"row": i, "error": str(e)})
        finally:
            driver.close()
        return {"inserted": inserted, "errors": errors}
