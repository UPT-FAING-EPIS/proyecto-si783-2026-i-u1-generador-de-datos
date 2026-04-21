namespace DataGenerator.API.Models;

public class DynamicTableRequest
{
    public string TableName { get; set; } = "tabla_dinamica";
    public int RecordCount { get; set; } = 100;
    public OutputFormat Format { get; set; } = OutputFormat.Sql;
    public DatabaseType DatabaseType { get; set; } = DatabaseType.MySQL;
    public List<ColumnDefinition> Columns { get; set; } = new();
}

public enum OutputFormat
{
    Sql = 0,
    Json = 1,
    Csv = 2,
    MongoDb = 3,    // ← Debe existir
    Redis = 4,
    Neo4j = 5,
    Cassandra = 6
}