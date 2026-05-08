from generators.field_mapper import generate_by_field_name
from generators.type_generator import generate_by_type
from schemas.connection import SchemaAnalysis, TableSchema, ColumnInfo
from typing import Optional
import random
import uuid

class DataGenerator:

    def __init__(self, schema: SchemaAnalysis, connector=None):
        self.schema = schema
        self.connector = connector
        self.generated_data: dict[str, list[dict]] = {}
        self._pk_pools: dict[str, list] = {}
        self._pk_offsets: dict[str, int] = {}
        self._existing_unique: dict[str, dict[str, set]] = {}

    def _get_table(self, name: str) -> Optional[TableSchema]:
        for t in self.schema.tables:
            if t.name == name:
                return t
        return None

    def _get_pk_col(self, table_name: str) -> Optional[ColumnInfo]:
        table = self._get_table(table_name)
        if not table:
            return None
        pks = [c for c in table.columns if c.is_primary_key]
        return pks[0] if pks else None

    def _is_auto_increment(self, col: ColumnInfo) -> bool:
        return col.default_value == "auto_increment"

    def _fetch_existing_unique(self, table_name: str):
        table = self._get_table(table_name)
        if not table or not self.connector:
            return
        self._existing_unique[table_name] = {}
        for col in table.columns:
            if col.is_unique and not col.is_primary_key:
                if hasattr(self.connector, "get_existing_values"):
                    try:
                        existing = self.connector.get_existing_values(table_name, col.name)
                        self._existing_unique[table_name][col.name] = existing
                    except:
                        self._existing_unique[table_name][col.name] = set()

    def _fetch_offset(self, table_name: str):
        pk_col = self._get_pk_col(table_name)
        if not pk_col:
            return
        if self._is_auto_increment(pk_col):
            if self.connector and hasattr(self.connector, "get_max_id"):
                try:
                    self._pk_offsets[table_name] = int(self.connector.get_max_id(table_name, pk_col.name))
                except:
                    self._pk_offsets[table_name] = 0
            return
        if self.connector and hasattr(self.connector, "get_max_id"):
            try:
                self._pk_offsets[table_name] = int(self.connector.get_max_id(table_name, pk_col.name))
            except:
                self._pk_offsets[table_name] = 0

    def _fetch_existing_ids(self, table_name: str):
        pk_col = self._get_pk_col(table_name)
        if not pk_col:
            return
        if self.connector and hasattr(self.connector, "get_existing_ids"):
            try:
                ids = self.connector.get_existing_ids(table_name, pk_col.name)
                if ids:
                    self._pk_pools[table_name] = ids
            except:
                pass

    def _build_pk_pool(self, table_name: str, count: int):
        pk_col = self._get_pk_col(table_name)
        if not pk_col:
            return
        dt = pk_col.data_type.lower()
        if dt in ("uuid", "uniqueidentifier"):
            self._pk_pools[table_name] = [str(uuid.uuid4()) for _ in range(count)]
            return
        if self._is_auto_increment(pk_col):
            offset = self._pk_offsets.get(table_name, 0)
            self._pk_pools[table_name] = list(range(offset + 1, offset + count + 1))
            return
        offset = self._pk_offsets.get(table_name, 0)
        self._pk_pools[table_name] = list(range(offset + 1, offset + count + 1))

    def _generate_value(self, col: ColumnInfo, row_index: int, table_name: str) -> any:
        if col.is_primary_key:
            if self._is_auto_increment(col):
                offset = self._pk_offsets.get(table_name, 0)
                return offset + row_index + 1
            pool = self._pk_pools.get(table_name, [])
            if pool and row_index < len(pool):
                return pool[row_index]
            offset = self._pk_offsets.get(table_name, 0)
            return offset + row_index + 1

        if col.is_foreign_key and col.references_table:
            ref_table = col.references_table
            if ref_table in self._pk_pools and self._pk_pools[ref_table]:
                return random.choice(self._pk_pools[ref_table])
            if ref_table in self.generated_data and self.generated_data[ref_table]:
                ref_rows = self.generated_data[ref_table]
                ref_table_obj = self._get_table(ref_table)
                if ref_table_obj:
                    ref_pk_cols = [c for c in ref_table_obj.columns if c.is_primary_key]
                    if ref_pk_cols:
                        valid = [r[ref_pk_cols[0].name] for r in ref_rows if r.get(ref_pk_cols[0].name) is not None]
                        if valid:
                            return random.choice(valid)
            offset = self._pk_offsets.get(ref_table, 0)
            if offset > 0:
                return random.randint(1, offset)
            return 1

        by_name = generate_by_field_name(col.name, table_name)
        if by_name is not None:
            return by_name

        return generate_by_type(col.data_type, col.max_length)

    def _topological_sort(self) -> list[str]:
        fk_deps: dict[str, set] = {t.name: set() for t in self.schema.tables}
        for rel in self.schema.relationships:
            child = rel.get("from_table")
            parent = rel.get("to_table")
            if child and parent and child != parent:
                fk_deps[child].add(parent)

        sorted_tables = []
        visited = set()

        def visit(name: str, chain: set):
            if name in chain:
                return
            if name in visited:
                return
            chain.add(name)
            for dep in fk_deps.get(name, []):
                visit(dep, chain)
            chain.discard(name)
            visited.add(name)
            sorted_tables.append(name)

        for table in self.schema.tables:
            visit(table.name, set())

        return sorted_tables

    def generate(self, table_name: str, count: int) -> list[dict]:
        table = self._get_table(table_name)
        if not table:
            return []

        self._fetch_offset(table_name)
        self._build_pk_pool(table_name, count)
        self._fetch_existing_unique(table_name)

        pk_col = self._get_pk_col(table_name)

        rows = []
        unique_tracker: dict[str, set] = {}
        for col in table.columns:
            if col.is_unique and not col.is_primary_key:
                existing = self._existing_unique.get(table_name, {}).get(col.name, set())
                unique_tracker[col.name] = set(existing)

        for i in range(count):
            row = {}
            for col in table.columns:
                value = self._generate_value(col, i, table_name)

                if col.is_unique and not col.is_primary_key and col.name in unique_tracker:
                    attempts = 0
                    while value in unique_tracker[col.name] and attempts < 200:
                        value = self._generate_value(col, i + attempts + 1000, table_name)
                        attempts += 1
                    unique_tracker[col.name].add(value)

                row[col.name] = value
            rows.append(row)

        self.generated_data[table_name] = rows

        if pk_col:
            self._pk_pools[table_name] = [r[pk_col.name] for r in rows if r.get(pk_col.name) is not None]

        return rows

    def generate_multiple(self, tables_counts: dict[str, int]) -> dict[str, list[dict]]:
        sorted_order = self._topological_sort()

        for table_name in sorted_order:
            self._fetch_offset(table_name)
            if table_name in tables_counts:
                self._build_pk_pool(table_name, tables_counts[table_name])
            else:
                self._fetch_existing_ids(table_name)

        results = {}
        for table_name in sorted_order:
            if table_name in tables_counts:
                rows = self.generate(table_name, tables_counts[table_name])
                results[table_name] = rows

        return results
