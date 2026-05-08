import time
from pymongo import MongoClient
from schemas.connection import ConnectionTest, SchemaAnalysis, TableSchema, ColumnInfo, ConnectionCreate
from connectors.base import BaseConnector
from datetime import datetime, timezone

class MongoDBConnector(BaseConnector):

    def _get_client(self):
        username = self.config.username or ""
        password = self.password or ""
        if username and password:
            uri = f"mongodb://{username}:{password}@{self.config.host}:{self.config.port}/"
        else:
            uri = f"mongodb://{self.config.host}:{self.config.port}/"
        return MongoClient(uri, serverSelectionTimeoutMS=5000)

    async def test_connection(self) -> ConnectionTest:
        try:
            t0 = time.time()
            client = self._get_client()
            info = client.server_info()
            client.close()
            return ConnectionTest(
                success=True,
                message="Conexion exitosa",
                engine_version=f"MongoDB {info.get('version','?')}",
                latency_ms=round((time.time()-t0)*1000, 2)
            )
        except Exception as e:
            return ConnectionTest(success=False, message=str(e))

    async def analyze_schema(self) -> SchemaAnalysis:
        client = self._get_client()
        tables = []
        try:
            db = client[self.config.database_name]
            collection_names = db.list_collection_names()

            for cname in collection_names:
                col = db[cname]
                row_count = col.count_documents({})
                sample = list(col.find({}, {"_id": 0}).limit(100))

                field_types: dict[str, set] = {}
                for doc in sample:
                    for field, value in doc.items():
                        dtype = type(value).__name__
                        if field not in field_types:
                            field_types[field] = set()
                        field_types[field].add(dtype)

                columns = [
                    ColumnInfo(
                        name="_id",
                        data_type="ObjectId",
                        is_nullable=False,
                        is_primary_key=True,
                        is_unique=True,
                        is_foreign_key=False,
                    )
                ]
                for fname, dtypes in field_types.items():
                    columns.append(ColumnInfo(
                        name=fname,
                        data_type=" | ".join(dtypes),
                        is_nullable=True,
                        is_primary_key=False,
                        is_unique=False,
                        is_foreign_key=False,
                    ))

                tables.append(TableSchema(name=cname, row_count=row_count, columns=columns))
        finally:
            client.close()

        return SchemaAnalysis(
            engine="mongodb",
            database=self.config.database_name,
            tables=tables,
            relationships=[],
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
        client = self._get_client()
        try:
            clean_records = []
            for r in records:
                doc = {k: v for k, v in r.items() if k != "_id" and v is not None}
                clean_records.append(doc)
            db = client[self.config.database_name]
            result = db[table].insert_many(clean_records, ordered=False)
            return {"inserted": len(result.inserted_ids), "errors": []}
        except Exception as e:
            return {"inserted": 0, "errors": [{"row": -1, "error": str(e)}]}
        finally:
            client.close()
