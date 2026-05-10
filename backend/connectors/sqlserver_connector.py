import time
import pyodbc
from schemas.connection import ConnectionTest, SchemaAnalysis, TableSchema, ColumnInfo, ConnectionCreate
from connectors.base import BaseConnector
from datetime import datetime, timezone

class SQLServerConnector(BaseConnector):

    def _get_conn(self):
        """
        Construye la cadena de conexión para SQL Server.
        
        Formato para pyodbc:
        "Driver={ODBC Driver 17 for SQL Server};Server=HOST,PORT;Database=DB;Uid=USER;Pwd=PASSWORD;"
        """
        driver = self.config.extra_params.get("driver", "ODBC Driver 17 for SQL Server") if self.config.extra_params else "ODBC Driver 17 for SQL Server"
        
        # Construir string de conexión
        conn_str = f"Driver={{{driver}}};Server={self.config.host},{self.config.port};Database={self.config.database_name};Uid={self.config.username};Pwd={self.password or ''};"
        
        # Si hay parámetros extra, agregarlos
        if self.config.extra_params:
            if "TrustServerCertificate" in self.config.extra_params:
                conn_str += f"TrustServerCertificate={self.config.extra_params['TrustServerCertificate']};"
            if "Encrypt" in self.config.extra_params:
                conn_str += f"Encrypt={self.config.extra_params['Encrypt']};"
            if "Connection Timeout" in self.config.extra_params:
                conn_str += f"Connection Timeout={self.config.extra_params['Connection Timeout']};"
        
        # Timeout por defecto
        if "Connection Timeout" not in (self.config.extra_params or {}):
            conn_str += "Connection Timeout=5;"
        
        try:
            return pyodbc.connect(conn_str, timeout=5)
        except Exception as e:
            raise Exception(f"Error al conectar a SQL Server: {str(e)}")

    async def test_connection(self) -> ConnectionTest:
        try:
            t0 = time.time()
            conn = self._get_conn()
            with conn.cursor() as cur:
                cur.execute("SELECT @@VERSION")
                version = cur.fetchone()[0].split(",")[0] if cur.fetchone() else "SQL Server"
            conn.close()
            return ConnectionTest(
                success=True, 
                message="Conexión exitosa", 
                engine_version=version, 
                latency_ms=round((time.time()-t0)*1000, 2)
            )
        except Exception as e:
            return ConnectionTest(success=False, message=str(e))

    async def analyze_schema(self) -> SchemaAnalysis:
        conn = self._get_conn()
        tables = []
        relationships = []
        
        try:
            with conn.cursor() as cur:
                # Obtener todas las tablas del schema
                cur.execute("""
                    SELECT TABLE_NAME 
                    FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_TYPE = 'BASE TABLE'
                    ORDER BY TABLE_NAME
                """)
                table_names = [row[0] for row in cur.fetchall()]

                for tname in table_names:
                    try:
                        cur.execute(f"SELECT COUNT(*) FROM [{tname}]")
                        row_count = cur.fetchone()[0]
                    except:
                        row_count = 0

                    # Obtener columnas con información de constraints
                    cur.execute(f"""
                        SELECT 
                            c.COLUMN_NAME, 
                            c.DATA_TYPE,
                            c.IS_NULLABLE,
                            c.CHARACTER_MAXIMUM_LENGTH,
                            c.COLUMN_DEFAULT,
                            CASE WHEN pk.COLUMN_NAME IS NOT NULL THEN 1 ELSE 0 END as is_pk,
                            CASE WHEN uq.COLUMN_NAME IS NOT NULL THEN 1 ELSE 0 END as is_uq
                        FROM INFORMATION_SCHEMA.COLUMNS c
                        LEFT JOIN (
                            SELECT ku.COLUMN_NAME 
                            FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc
                            JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE ku 
                                ON tc.CONSTRAINT_NAME = ku.CONSTRAINT_NAME
                            WHERE tc.TABLE_NAME = ? AND tc.CONSTRAINT_TYPE = 'PRIMARY KEY'
                        ) pk ON c.COLUMN_NAME = pk.COLUMN_NAME
                        LEFT JOIN (
                            SELECT ku.COLUMN_NAME 
                            FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc
                            JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE ku 
                                ON tc.CONSTRAINT_NAME = ku.CONSTRAINT_NAME
                            WHERE tc.TABLE_NAME = ? AND tc.CONSTRAINT_TYPE = 'UNIQUE'
                        ) uq ON c.COLUMN_NAME = uq.COLUMN_NAME
                        WHERE c.TABLE_NAME = ?
                        ORDER BY c.ORDINAL_POSITION
                    """, (tname, tname, tname))
                    raw_cols = cur.fetchall()

                    # Obtener Foreign Keys
                    cur.execute(f"""
                        SELECT 
                            kcu.COLUMN_NAME,
                            ccu.TABLE_NAME,
                            ccu.COLUMN_NAME
                        FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc
                        JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE kcu 
                            ON tc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
                        JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE ccu 
                            ON tc.CONSTRAINT_NAME = ccu.CONSTRAINT_NAME
                        WHERE tc.TABLE_NAME = ? AND tc.CONSTRAINT_TYPE = 'FOREIGN KEY'
                    """, (tname,))
                    fk_rows = {row[0]: (row[1], row[2]) for row in cur.fetchall()}

                    columns = []
                    for col in raw_cols:
                        col_name, data_type, nullable, max_len, default, is_pk, is_uq = col
                        is_fk = col_name in fk_rows
                        ref_table, ref_col = fk_rows.get(col_name, (None, None))
                        
                        if is_fk:
                            relationships.append({
                                "from_table": tname, 
                                "from_column": col_name, 
                                "to_table": ref_table, 
                                "to_column": ref_col
                            })
                        
                        columns.append(ColumnInfo(
                            name=col_name, 
                            data_type=data_type,
                            is_nullable=(nullable == "YES"), 
                            is_primary_key=bool(is_pk),
                            is_unique=bool(is_uq), 
                            is_foreign_key=is_fk,
                            references_table=ref_table, 
                            references_column=ref_col,
                            default_value=str(default) if default else None, 
                            max_length=max_len,
                        ))
                    
                    tables.append(TableSchema(name=tname, row_count=row_count, columns=columns))
        finally:
            conn.close()

        return SchemaAnalysis(
            engine="sqlserver", 
            database=self.config.database_name,
            tables=tables, 
            relationships=relationships,
            total_tables=len(tables), 
            analyzed_at=datetime.now(timezone.utc),
        )

    async def execute_inserts(self, table: str, records: list[dict]) -> dict:
        if not records:
            return {"inserted": 0, "errors": []}
        
        conn = self._get_conn()
        inserted = 0
        errors = []
        
        try:
            with conn.cursor() as cur:
                cols = ", ".join(f"[{k}]" for k in records[0].keys())
                placeholders = ", ".join(["?"] * len(records[0]))
                sql = f"INSERT INTO [{table}] ({cols}) VALUES ({placeholders})"
                
                for i, record in enumerate(records):
                    try:
                        cur.execute(sql, list(record.values()))
                        inserted += 1
                    except Exception as e:
                        errors.append({"row": i, "error": str(e)})
            
            conn.commit()
        except Exception as e:
            errors.append({"general": str(e)})
        finally:
            conn.close()

        return {"inserted": inserted, "errors": errors}
