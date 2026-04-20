using DataGenerator.API.Models;
using DataGenerator.API.Adapters;
using System.Text;

namespace DataGenerator.API.Exporters;

public class SqlDynamicExporter : IDynamicExporter
{
    private readonly IDatabaseAdapter _adapter;
    
    public SqlDynamicExporter(DatabaseType databaseType)
    {
        _adapter = databaseType switch
        {
            DatabaseType.MySQL => new MySqlAdapter(),
            DatabaseType.PostgreSQL => new PostgreSqlAdapter(),
            DatabaseType.MicrosoftSQLServer => new SqlServerAdapter(),
            _ => new MySqlAdapter()
        };
    }
    
    public string Export(List<Dictionary<string, object>> data, DynamicTableRequest request)
    {
        var sb = new StringBuilder();
        
        // 1. Agregar DDL (CREATE TABLE)
        sb.AppendLine(_adapter.GetCreateTableScript(request.TableName, request.Columns));
        sb.AppendLine();
        
        // 2. Agregar INSERTs
        foreach (var row in data)
        {
            sb.AppendLine(_adapter.GetInsertScript(request.TableName, request.Columns, row));
        }
        
        return sb.ToString();
    }
    
    public string GetFileExtension() => ".sql";
}