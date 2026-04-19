using System.Text.Json;
using DataGenerator.API.Models;

namespace DataGenerator.API.Exporters;

public class JsonDynamicExporter : IDynamicExporter
{
    private readonly JsonSerializerOptions _options = new() 
    { 
        WriteIndented = true,
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase
    };
    
    public string Export(List<Dictionary<string, object>> data, DynamicTableRequest request)
    {
        return JsonSerializer.Serialize(new
        {
            tableName = request.TableName,
            recordCount = data.Count,
            generatedAt = DateTime.Now,
            data = data
        }, _options);
    }
    
    public string GetFileExtension() => ".json";
}