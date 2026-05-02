using System.ComponentModel.DataAnnotations;

namespace DataGenerator.API.Models;

public class DynamicTableRequest
{
    [Required]
    [MinLength(1)]
    public string TableName { get; set; } = "tabla_dinamica";

    [Range(1, 50000, ErrorMessage = "RecordCount debe estar entre 1 y 50.000")]
    public int RecordCount { get; set; } = 100;

    public OutputFormat Format { get; set; } = OutputFormat.Sql;
    public DatabaseType DatabaseType { get; set; } = DatabaseType.MySQL;

    [Required]
    [MinLength(1, ErrorMessage = "Debes definir al menos una columna")]
    public List<ColumnDefinition> Columns { get; set; } = new();
}

public enum OutputFormat
{
    Sql           = 0,
    Json          = 1,
    Csv           = 2,
    MongoDb       = 3,
    Redis         = 4,
    Neo4j         = 5,
    Cassandra     = 6,
    Elasticsearch = 7,
    InfluxDb      = 8,
    DynamoDb      = 9
}