from schemas.connection import ConnectionCreate, DBEngine
from connectors.base import BaseConnector
from connectors.mysql_connector import MySQLConnector
from connectors.postgresql_connector import PostgreSQLConnector
from connectors.mongodb_connector import MongoDBConnector
from connectors.redis_connector import RedisConnector
from connectors.neo4j_connector import Neo4jConnector
from fastapi import HTTPException

def get_connector(config: ConnectionCreate, password: str = None) -> BaseConnector:
    connectors = {
        DBEngine.mysql: MySQLConnector,
        DBEngine.postgresql: PostgreSQLConnector,
        DBEngine.mongodb: MongoDBConnector,
        DBEngine.redis: RedisConnector,
        DBEngine.neo4j: Neo4jConnector,
    }
    cls = connectors.get(config.engine)
    if not cls:
        raise HTTPException(status_code=400, detail=f"Motor '{config.engine}' no soportado aún")
    return cls(config, password)
