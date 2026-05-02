namespace DataGenerator.API.Models;

public enum DatabaseType
{
    // SQL Relacional
    MySQL              = 0,
    PostgreSQL         = 1,
    MicrosoftSQLServer = 2,
    Oracle             = 3,

    // NoSQL Documental
    MongoDB            = 10,

    // NoSQL Clave-Valor
    Redis              = 11,
    DynamoDB           = 12,

    // NoSQL Búsqueda
    Elasticsearch      = 13,

    // NoSQL Grafo
    Neo4j              = 14,

    // NoSQL Columnar
    Cassandra          = 15,

    // Series de Tiempo
    InfluxDB           = 16
}