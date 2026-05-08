from faker import Faker
import random
import uuid
from datetime import datetime, timezone

fake = Faker("es_ES")

def generate_by_type(data_type: str, max_length: int = None) -> any:
    dt = data_type.lower().strip()

    if dt in ("varchar", "character varying", "nvarchar"):
        length = min(max_length or 50, 50)
        return fake.lexify(text="?" * min(length, 10))

    if dt in ("text", "longtext", "mediumtext", "tinytext", "clob"):
        return fake.paragraph(nb_sentences=2)

    if dt in ("int", "integer", "smallint", "tinyint", "mediumint"):
        return random.randint(1, 9999)

    if dt in ("bigint",):
        return random.randint(1, 999999)

    if dt in ("float", "double", "real", "double precision"):
        return round(random.uniform(1.0, 9999.99), 4)

    if dt in ("decimal", "numeric", "money"):
        return round(random.uniform(1.0, 9999.99), 2)

    if dt in ("boolean", "bool", "tinyint(1)"):
        return random.choice([True, False])

    if dt in ("date",):
        return fake.date_this_decade().isoformat()

    if dt in ("datetime", "timestamp", "timestamp with time zone", "timestamp without time zone"):
        return fake.date_time_this_decade().isoformat()

    if dt in ("time",):
        return fake.time()

    if dt in ("year",):
        return random.randint(2000, 2026)

    if dt in ("uuid", "uniqueidentifier"):
        return str(uuid.uuid4())

    if dt in ("json", "jsonb"):
        return {"key": fake.word(), "value": fake.word(), "active": True}

    if dt in ("array",):
        return [fake.word() for _ in range(random.randint(1, 5))]

    if dt in ("char", "nchar", "character"):
        return fake.lexify(text="?")

    if dt in ("binary", "varbinary", "blob"):
        return None

    if dt in ("enum",):
        return random.choice(["opcion_a", "opcion_b", "opcion_c"])

    return fake.word()
