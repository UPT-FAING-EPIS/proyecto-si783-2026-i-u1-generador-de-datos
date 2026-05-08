import time
import pymysql
from schemas.connection import ConnectionTest, SchemaAnalysis, TableSchema, ColumnInfo, ConnectionCreate
from connectors.base import BaseConnector
from datetime import datetime, timezone

class MySQLConnector(BaseConnector):

    def _get_conn(self):
        return pymysql.connect(
            host=self.config.host,
            port=self.config.port,
            user=self.config.username,
            password=self.password or "",
            database=self.config.database_name,
            connect_timeout=5,
            charset="utf8mb4",
        )

    async def test_connection(self) -> ConnectionTest:
        try:
            t0 = time.time()
            conn = self._get_conn()
            with conn.cursor() as cur:
                cur.execute("SELECT VERSION()")
                version = cur.fetchone()[0]
            conn.close()
            return ConnectionTest(success=True, message="Conexion exitosa", engine_version=f"MySQL {version}", latency_ms=round((time.time()-t0)*1000, 2))
        except Exception as e:
            return ConnectionTest(success=False, message=str(e))

    async def analyze_schema(self) -> SchemaAnalysis:
        conn = self._get_conn()
        tables = []
        relationships = []
        try:
            with conn.cursor() as cur:
                cur.execute("SHOW TABLES")
                table_names = [row[0] for row in cur.fetchall()]

                for tname in table_names:
                    cur.execute(f"SELECT COUNT(*) FROM `{tname}`")
                    row_count = cur.fetchone()[0]

                    cur.execute(f"""
                        SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_KEY,
                               CHARACTER_MAXIMUM_LENGTH, COLUMN_DEFAULT, EXTRA
                        FROM INFORMATION_SCHEMA.COLUMNS
                        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
                        ORDER BY ORDINAL_POSITION
                    """, (self.config.database_name, tname))
                    raw_cols = cur.fetchall()

                    cur.execute(f"""
                        SELECT COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
                        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
                        AND REFERENCED_TABLE_NAME IS NOT NULL
                    """, (self.config.database_name, tname))
                    fk_rows = {row[0]: (row[1], row[2]) for row in cur.fetchall()}

                    cur.execute(f"""
                        SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.STATISTICS
                        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
                        AND NON_UNIQUE = 0 AND INDEX_NAME != 'PRIMARY'
                    """, (self.config.database_name, tname))
                    unique_cols = {row[0] for row in cur.fetchall()}

                    columns = []
                    for col in raw_cols:
                        col_name, data_type, nullable, col_key, max_len, default, extra = col
                        is_fk = col_name in fk_rows
                        ref_table, ref_col = fk_rows.get(col_name, (None, None))
                        is_auto = "auto_increment" in (extra or "").lower()
                        if is_fk:
                            relationships.append({"from_table": tname, "from_column": col_name, "to_table": ref_table, "to_column": ref_col})
                        columns.append(ColumnInfo(
                            name=col_name, data_type=data_type,
                            is_nullable=(nullable == "YES"),
                            is_primary_key=(col_key == "PRI"),
                            is_unique=(col_name in unique_cols or col_key == "UNI"),
                            is_foreign_key=is_fk,
                            references_table=ref_table, references_column=ref_col,
                            default_value="auto_increment" if is_auto else (str(default) if default else None),
                            max_length=max_len,
                        ))
                    tables.append(TableSchema(name=tname, row_count=row_count, columns=columns))
        finally:
            conn.close()

        return SchemaAnalysis(
            engine="mysql", database=self.config.database_name,
            tables=tables, relationships=relationships,
            total_tables=len(tables), analyzed_at=datetime.now(timezone.utc),
        )

    def get_max_id(self, table: str, pk_col: str) -> int:
        conn = self._get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(f"SELECT COALESCE(MAX(`{pk_col}`), 0) FROM `{table}`")
                return cur.fetchone()[0]
        finally:
            conn.close()

    def get_existing_ids(self, table: str, pk_col: str) -> list:
        conn = self._get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(f"SELECT `{pk_col}` FROM `{table}`")
                return [row[0] for row in cur.fetchall()]
        finally:
            conn.close()

    def get_existing_values(self, table: str, col: str) -> set:
        conn = self._get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(f"SELECT `{col}` FROM `{table}`")
                return {row[0] for row in cur.fetchall()}
        finally:
            conn.close()

    async def execute_inserts(self, table: str, records: list[dict]) -> dict:
        if not records:
            return {"inserted": 0, "errors": []}
        conn = self._get_conn()
        inserted = 0
        errors = []
        try:
            with conn.cursor() as cur:
                cols = ", ".join(f"`{k}`" for k in records[0].keys())
                placeholders = ", ".join(["%s"] * len(records[0]))
                sql = f"INSERT INTO `{table}` ({cols}) VALUES ({placeholders})"
                for i, record in enumerate(records):
                    try:
                        cur.execute(sql, list(record.values()))
                        inserted += 1
                    except Exception as e:
                        errors.append({"row": i, "error": str(e)})
            conn.commit()
        except Exception as e:
            conn.rollback()
            errors.append({"row": -1, "error": str(e)})
        finally:
            conn.close()
        return {"inserted": inserted, "errors": errors}
