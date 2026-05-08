from abc import ABC, abstractmethod
from schemas.connection import ConnectionTest, SchemaAnalysis, ConnectionCreate

class BaseConnector(ABC):

    def __init__(self, config: ConnectionCreate, password: str = None):
        self.config = config
        self.password = password

    @abstractmethod
    async def test_connection(self) -> ConnectionTest:
        pass

    @abstractmethod
    async def analyze_schema(self) -> SchemaAnalysis:
        pass

    @abstractmethod
    async def execute_inserts(self, table: str, records: list[dict]) -> dict:
        pass
