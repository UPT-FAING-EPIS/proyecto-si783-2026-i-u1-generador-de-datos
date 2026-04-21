namespace DataGenerator.API.Models;

public enum DatabaseType
{
    // SQL
    MySQL = 0,
    PostgreSQL = 1,
    MicrosoftSQLServer = 2,
    Oracle = 3,
    
    // NoSQL
    MongoDB = 10,
    Redis = 11,
    Elasticsearch = 12,
    Neo4j = 13,
    Cassandra = 14,
    InfluxDB = 15,
    DynamoDB = 16
}