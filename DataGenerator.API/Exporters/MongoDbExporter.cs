using DataGenerator.API.Models;
using System.Text;

namespace DataGenerator.API.Exporters;

public class MongoDbExporter : IDynamicExporter
{
    public string Export(List<Dictionary<string, object>> data, DynamicTableRequest request)
    {
        var sb = new StringBuilder();
        
        // ✅ SOLO el array de documentos, sin metadata
        sb.AppendLine("[");
        
        for (int i = 0; i < data.Count; i++)
        {
            var row = data[i];
            sb.AppendLine("  {");
            
            var fields = new List<string>();
            foreach (var col in request.Columns)
            {
                var value = row[col.Name];
                string formattedValue = FormatMongoValue(value);
                fields.Add($"    \"{col.Name}\": {formattedValue}");
            }
            
            sb.Append(string.Join(",\n", fields));
            sb.Append("\n  }");
            
            if (i < data.Count - 1)
                sb.AppendLine(",");
            else
                sb.AppendLine();
        }
        
        sb.AppendLine("]");
        return sb.ToString();
    }
    
    private string FormatMongoValue(object value)
    {
        if (value == null) return "null";
        
        if (value is bool b) return b ? "true" : "false";
        if (value is int || value is long || value is decimal || value is double || value is float)
            return value.ToString()?.Replace(",", ".") ?? "0";
        if (value is DateTime dt)
            return $"\"{dt:yyyy-MM-ddTHH:mm:ss.fffZ}\"";
        
        // String
        return $"\"{value.ToString()?.Replace("\"", "\\\"")}\"";
    }
    
    public string GetFileExtension() => "json";
}