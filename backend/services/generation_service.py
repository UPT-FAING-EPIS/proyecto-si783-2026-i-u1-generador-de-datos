from sqlalchemy.ext.asyncio import AsyncSession
from schemas.generation import GenerationRequest, GenerationResponse, GenerationResult, GenerationPreview, InsertPreviewRequest
from schemas.connection import DBEngine, ConnectionCreate
from services.connection_service import get_connection_by_id, analyze_connection_service
from connectors.factory import get_connector
from core.encryption import decrypt_password
from generators.data_generator import DataGenerator
from uuid import UUID

async def _get_connector(db, db_conn):
    from schemas.connection import DBEngine, ConnectionCreate
    config = ConnectionCreate(
        name=db_conn.name,
        engine=DBEngine(db_conn.engine),
        host=db_conn.host,
        port=db_conn.port,
        username=db_conn.username or None,
        database_name=db_conn.database_name,
        extra_params=db_conn.extra_params,
    )
    password = decrypt_password(db_conn.encrypted_password) if db_conn.encrypted_password else None
    return get_connector(config, password)

async def generate_data_service(
    db: AsyncSession,
    user_id: UUID,
    request: GenerationRequest,
) -> GenerationResponse:

    db_conn = await get_connection_by_id(db, request.connection_id, user_id)
    schema = await analyze_connection_service(db, request.connection_id, user_id)
    connector = await _get_connector(db, db_conn)

    tables_counts = {t.table_name: t.count for t in request.tables}
    generator = DataGenerator(schema, connector=connector)
    all_data = generator.generate_multiple(tables_counts)

    if request.preview_only:
        previews = []
        for table_name, rows in all_data.items():
            previews.append(GenerationPreview(
                table_name=table_name,
                count=len(rows),
                sample=rows[:5],
                all_data=rows,
            ))
        return GenerationResponse(
            connection_id=str(request.connection_id),
            engine=schema.engine,
            database=schema.database,
            previews=previews,
            preview_only=True,
        )

    results = []
    total_inserted = 0
    total_errors = 0

    for table_name, rows in all_data.items():
        if not rows:
            continue
        insert_result = await connector.execute_inserts(table_name, rows)
        inserted = insert_result.get("inserted", 0)
        errors = insert_result.get("errors", [])
        total_inserted += inserted
        total_errors += len(errors)
        results.append(GenerationResult(
            table_name=table_name,
            requested=len(rows),
            inserted=inserted,
            errors=errors,
        ))

    return GenerationResponse(
        connection_id=str(request.connection_id),
        engine=schema.engine,
        database=schema.database,
        results=results,
        total_inserted=total_inserted,
        total_errors=total_errors,
        preview_only=False,
    )

async def insert_preview_service(
    db: AsyncSession,
    user_id: UUID,
    request: InsertPreviewRequest,
) -> GenerationResponse:

    db_conn = await get_connection_by_id(db, request.connection_id, user_id)
    schema = await analyze_connection_service(db, request.connection_id, user_id)
    connector = await _get_connector(db, db_conn)

    results = []
    total_inserted = 0
    total_errors = 0

    from generators.data_generator import DataGenerator
    generator = DataGenerator(schema, connector=connector)
    sorted_tables = generator._topological_sort()

    ordered_data = {}
    for table_name in sorted_tables:
        if table_name in request.confirmed_data:
            ordered_data[table_name] = request.confirmed_data[table_name]

    for table_name, rows in ordered_data.items():
        if not rows:
            continue
        insert_result = await connector.execute_inserts(table_name, rows)
        inserted = insert_result.get("inserted", 0)
        errors = insert_result.get("errors", [])
        total_inserted += inserted
        total_errors += len(errors)
        results.append(GenerationResult(
            table_name=table_name,
            requested=len(rows),
            inserted=inserted,
            errors=errors,
        ))

    return GenerationResponse(
        connection_id=str(request.connection_id),
        engine=schema.engine,
        database=schema.database,
        results=results,
        total_inserted=total_inserted,
        total_errors=total_errors,
        preview_only=False,
    )
