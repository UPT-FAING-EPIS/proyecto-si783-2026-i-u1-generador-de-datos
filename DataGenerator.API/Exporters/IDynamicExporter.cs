using DataGenerator.API.Models;

namespace DataGenerator.API.Exporters;

public interface IDynamicExporter
{
    string Export(List<Dictionary<string, object>> data, DynamicTableRequest request);
    string GetFileExtension();
}