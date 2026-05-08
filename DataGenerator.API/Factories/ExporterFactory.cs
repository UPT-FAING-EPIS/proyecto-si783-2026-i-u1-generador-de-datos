using DataGenerator.API.Exporters;
using DataGenerator.API.Models;

namespace DataGenerator.API.Factories;

public class ExporterFactory : IExporterFactory
{
    public IDynamicExporter Create(OutputFormat format, DatabaseType databaseType)
    {
        return format switch
        {
            OutputFormat.Sql           => new SqlDynamicExporter(databaseType),
            OutputFormat.Json          => new JsonDynamicExporter(),
            OutputFormat.Csv           => new CsvDynamicExporter(),
            OutputFormat.MongoDb       => new MongoDbExporter(),
            OutputFormat.Redis         => new RedisExporter(),
            OutputFormat.Neo4j         => new Neo4jExporter(),
            OutputFormat.Cassandra     => new CassandraExporter(),
            OutputFormat.Elasticsearch => new ElasticsearchExporter(),
            OutputFormat.InfluxDb      => new InfluxDbExporter(),
            OutputFormat.DynamoDb      => new DynamoDbExporter(),
            _                          => new JsonDynamicExporter()
        };
    }
}