using System.Text;
using DataGenerator.API.Models;

namespace DataGenerator.API.Exporters;

public class CsvDynamicExporter : IDynamicExporter
{
    public string Export(List<Dictionary<string, object>> data, DynamicTableRequest request)
    {
        if (!data.Any()) return string.Empty;
        
        var csv = new StringBuilder();
        
        // Headers
        var headers = data.First().Keys;
        csv.AppendLine(string.Join(",", headers.Select(EscapeCsvValue)));
        
        // Data rows
        foreach (var row in data)
        {
            var values = headers.Select(h => EscapeCsvValue(row[h]?.ToString() ?? ""));
            csv.AppendLine(string.Join(",", values));
        }
        
        return csv.ToString();
    }
    
    private string EscapeCsvValue(string value)
    {
        if (value.Contains(",") || value.Contains("\"") || value.Contains("\n"))
        {
            return $"\"{value.Replace("\"", "\"\"")}\"";
        }
        return value;
    }
    
    public string GetFileExtension() => ".csv";
}