using DataGenerator.API.Models;
using System.Text;

namespace DataGenerator.API.Exporters;

public class Neo4jExporter : IDynamicExporter
{
    public string Export(List<Dictionary<string, object>> data, DynamicTableRequest request)
    {
        var sb = new StringBuilder();
        
        sb.AppendLine($"// Cypher for {request.TableName}");
        sb.AppendLine();
        
        foreach (var row in data)
        {
            var props = new List<string>();
            foreach (var col in request.Columns)
            {
                var value = row[col.Name];
                string formattedValue = FormatCypherValue(value);
                props.Add($"{col.Name}: {formattedValue}");
            }
            
            sb.AppendLine($"CREATE (n:{request.TableName} {{{string.Join(", ", props)}}});");
        }
        
        return sb.ToString();
    }
    
    private string FormatCypherValue(object value)
    {
        if (value == null) return "null";
        
        if (value is bool b) return b ? "true" : "false";
        if (value is int || value is long || value is decimal || value is double)
            return value.ToString() ?? "0";
        if (value is DateTime dt)
            return $"datetime('{dt:yyyy-MM-ddTHH:mm:ss}Z')";
        
        return $"'{value.ToString()?.Replace("'", "\\'")}'";
    }
    
    public string GetFileExtension() => ".cypher";
}