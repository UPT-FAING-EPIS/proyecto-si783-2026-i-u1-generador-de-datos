using DataGenerator.API.Models;
using System.Text;

namespace DataGenerator.API.Exporters;

public class CassandraExporter : IDynamicExporter
{
    public string Export(List<Dictionary<string, object>> data, DynamicTableRequest request)
    {
        var sb = new StringBuilder();
        
        // CREATE TABLE
        var columnsDef = new List<string>();
        foreach (var col in request.Columns)
        {
            string type = GetCqlType(col.Type);
            columnsDef.Add($"{col.Name} {type}");
        }
        
        sb.AppendLine($"CREATE TABLE IF NOT EXISTS {request.TableName} (");
        sb.AppendLine($"  {string.Join(",\n  ", columnsDef)}");
        sb.AppendLine(");");
        sb.AppendLine();
        
        // INSERTs
        foreach (var row in data)
        {
            var names = request.Columns.Select(c => c.Name);
            var values = request.Columns.Select(c => FormatCqlValue(row[c.Name], c.Type));
            
            sb.AppendLine($"INSERT INTO {request.TableName} ({string.Join(", ", names)}) VALUES ({string.Join(", ", values)});");
        }
        
        return sb.ToString();
    }
    
    private string GetCqlType(DataType type)
    {
        return type switch
        {
            DataType.Integer => "int",
            DataType.Decimal => "decimal",
            DataType.String => "text",
            DataType.Boolean => "boolean",
            DataType.DateTime => "timestamp",
            DataType.Date => "date",
            _ => "text"
        };
    }
    
    private string FormatCqlValue(object value, DataType type)
    {
        if (value == null) return "null";
        
        if (type == DataType.Boolean) return (bool)value ? "true" : "false";
        if (type == DataType.Integer || type == DataType.Decimal)
            return value.ToString() ?? "0";
        if (type == DataType.DateTime && value is DateTime dt)
            return $"'{dt:yyyy-MM-dd HH:mm:ss}'";
        
        return $"'{value.ToString()?.Replace("'", "''")}'";
    }
    
    public string GetFileExtension() => "cql";
}