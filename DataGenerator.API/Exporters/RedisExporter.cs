using DataGenerator.API.Models;
using System.Text;

namespace DataGenerator.API.Exporters;

public class RedisExporter : IDynamicExporter
{
    public string Export(List<Dictionary<string, object>> data, DynamicTableRequest request)
    {
        var sb = new StringBuilder();
        
        sb.AppendLine($"# Redis commands for {request.TableName}");
        sb.AppendLine();
        
        for (int i = 0; i < data.Count; i++)
        {
            var row = data[i];
            var id = row.ContainsKey("id") ? row["id"] : i.ToString();
            
            sb.AppendLine($"HSET {request.TableName}:{id}");
            foreach (var col in request.Columns)
            {
                var value = row[col.Name];
                string formattedValue = FormatRedisValue(value);
                sb.AppendLine($"  {col.Name} {formattedValue}");
            }
            if (i < data.Count - 1) sb.AppendLine();
        }
        
        return sb.ToString();
    }
    
    private string FormatRedisValue(object value)
    {
        if (value == null) return "\"\"";
        
        if (value is bool b) return b ? "1" : "0";
        if (value is int || value is long || value is decimal || value is double)
            return value.ToString() ?? "0";
        
        return $"\"{value}\"";
    }
    
    public string GetFileExtension() => "redis";
}