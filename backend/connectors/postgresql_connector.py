import time
import psycopg2
from schemas.connection import ConnectionTest, SchemaAnalysis, TableSchema, ColumnInfo, ConnectionCreate
from connectors.base import BaseConnector
from datetime import datetime, timezone

class PostgreSQLConnector(BaseConnector):

    def _get_conn(self):
        return psycopg2.connect(
            host=self.config.host, port=self.config.port,
            user=self.config.username, password=self.password or "",
            dbname=self.config.database_name, connect_timeout=5,
        )

    async def test_connection(self) -> ConnectionTest:
        try:
            t0 = time.time()
            conn = self._get_conn()
            with conn.cursor() as cur:
                cur.execute("SELECT version()")
                version = cur.fetchone()[0].split(",")[0]
            conn.close()
            return ConnectionTest(success=True, message="Conexión exitosa", engine_version=version, latency_ms=round((time.time()-t0)*1000, 2))
        except Exception as e:
            return ConnectionTest(success=False, message=str(e))

    async def analyze_schema(self) -> SchemaAnalysis:
        conn = self._get_conn()
        tables = []
        relationships = []
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT table_name FROM information_schema.tables
                    WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
                    ORDER BY table_name
                """)
                table_names = [row[0] for row in cur.fetchall()]

                for tname in table_names:
                    try:
                        cur.execute(f'SELECT COUNT(*) FROM "{tname}"')
                        row_count = cur.fetchone()[0]
                    except:
                        row_count = 0

                    cur.execute("""
                        SELECT c.column_name, c.data_type, c.is_nullable,
                               c.character_maximum_length, c.column_default,
                               CASE WHEN pk.column_name IS NOT NULL THEN true ELSE false END as is_pk,
                               CASE WHEN uq.column_name IS NOT NULL THEN true ELSE false END as is_uq
                        FROM information_schema.columns c
                        LEFT JOIN (
                            SELECT ku.column_name FROM information_schema.table_constraints tc
                            JOIN information_schema.key_column_usage ku ON tc.constraint_name = ku.constraint_name
                            WHERE tc.table_name = %s AND tc.constraint_type = 'PRIMARY KEY'
                        ) pk ON c.column_name = pk.column_name
                        LEFT JOIN (
                            SELECT ku.column_name FROM information_schema.table_constraints tc
                            JOIN information_schema.key_column_usage ku ON tc.constraint_name = ku.constraint_name
                            WHERE tc.table_name = %s AND tc.constraint_type = 'UNIQUE'
                        ) uq ON c.column_name = uq.column_name
                        WHERE c.table_name = %s AND c.table_schema = 'public'
                        ORDER BY c.ordinal_position
                    """, (tname, tname, tname))
                    raw_cols = cur.fetchall()

                    cur.execute("""
                        SELECT kcu.column_name, ccu.table_name, ccu.column_name
                        FROM information_schema.table_constraints tc
                        JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name
                        JOIN information_schema.constraint_column_usage ccu ON tc.constraint_name = ccu.constraint_name
                        WHERE tc.table_name = %s AND tc.constraint_type = 'FOREIGN KEY'
                    """, (tname,))
                    fk_rows = {row[0]: (row[1], row[2]) for row in cur.fetchall()}

                    columns = []
                    for col in raw_cols:
                        col_name, data_type, nullable, max_len, default, is_pk, is_uq = col
                        is_fk = col_name in fk_rows
                        ref_table, ref_col = fk_rows.get(col_name, (None, None))
                        if is_fk:
                            relationships.append({"from_table": tname, "from_column": col_name, "to_table": ref_table, "to_column": ref_col})
                        columns.append(ColumnInfo(
                            name=col_name, data_type=data_type,
                            is_nullable=(nullable == "YES"), is_primary_key=bool(is_pk),
                            is_unique=bool(is_uq), is_foreign_key=is_fk,
                            references_table=ref_table, references_column=ref_col,
                            default_value=str(default) if default else None, max_length=max_len,
                        ))
                    tables.append(TableSchema(name=tname, row_count=row_count, columns=columns))
        finally:
            conn.close()

        return SchemaAnalysis(
            engine="postgresql", database=self.config.database_name,
            tables=tables, relationships=relationships,
            total_tables=len(tables), analyzed_at=datetime.now(timezone.utc),
        )

    async def execute_inserts(self, table: str, records: list[dict]) -> dict:
        if not records:
            return {"inserted": 0, "errors": []}
        conn = self._get_conn()
        inserted = 0
        errors = []
        try:
            with conn.cursor() as cur:
                cols = ", ".join(f'"{k}"' for k in records[0].keys())
                placeholders = ", ".join(["%s"] * len(records[0]))
                sql = f'INSERT INTO "{table}" ({cols}) VALUES ({placeholders})'
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
