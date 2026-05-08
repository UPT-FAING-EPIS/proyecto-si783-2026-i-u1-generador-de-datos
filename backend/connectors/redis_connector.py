import time
import redis as redis_lib
from schemas.connection import ConnectionTest, SchemaAnalysis, TableSchema, ColumnInfo, ConnectionCreate
from connectors.base import BaseConnector
from datetime import datetime, timezone

class RedisConnector(BaseConnector):

    def _get_client(self):
        return redis_lib.Redis(
            host=self.config.host, port=self.config.port,
            password=self.password or None, decode_responses=True,
            socket_connect_timeout=5,
        )

    async def test_connection(self) -> ConnectionTest:
        try:
            t0 = time.time()
            r = self._get_client()
            info = r.info("server")
            r.close()
            return ConnectionTest(success=True, message="Conexión exitosa", engine_version=f"Redis {info.get('redis_version','?')}", latency_ms=round((time.time()-t0)*1000, 2))
        except Exception as e:
            return ConnectionTest(success=False, message=str(e))

    async def analyze_schema(self) -> SchemaAnalysis:
        r = self._get_client()
        try:
            info = r.info()
            keys = r.keys("*")[:100]
            key_types = {}
            for key in keys:
                try:
                    ktype = r.type(key)
                    key_types[ktype] = key_types.get(ktype, 0) + 1
                except:
                    pass

            columns = [
                ColumnInfo(name="key", data_type="string", is_nullable=False, is_primary_key=True, is_unique=True, is_foreign_key=False),
                ColumnInfo(name="value", data_type="mixed", is_nullable=True, is_primary_key=False, is_unique=False, is_foreign_key=False),
                ColumnInfo(name="type", data_type="string", is_nullable=False, is_primary_key=False, is_unique=False, is_foreign_key=False),
                ColumnInfo(name="ttl", data_type="integer", is_nullable=True, is_primary_key=False, is_unique=False, is_foreign_key=False),
            ]

            table = TableSchema(name="keyspace", row_count=info.get("db0", {}).get("keys", len(keys)), columns=columns)
        finally:
            r.close()

        return SchemaAnalysis(
            engine="redis", database=str(self.config.database_name or "0"),
            tables=[table], relationships=[],
            total_tables=1, analyzed_at=datetime.now(timezone.utc),
        )

    async def execute_inserts(self, table: str, records: list[dict]) -> dict:
        r = self._get_client()
        inserted = 0
        errors = []
        try:
            pipe = r.pipeline()
            for i, record in enumerate(records):
                key = record.get("key")
                value = record.get("value", "")
                ttl = record.get("ttl")
                if not key:
                    errors.append({"row": i, "error": "Falta campo 'key'"})
                    continue
                pipe.set(key, str(value))
                if ttl:
                    pipe.expire(key, int(ttl))
                inserted += 1
            pipe.execute()
        except Exception as e:
            errors.append({"row": -1, "error": str(e)})
        finally:
            r.close()
        return {"inserted": inserted, "errors": errors}
