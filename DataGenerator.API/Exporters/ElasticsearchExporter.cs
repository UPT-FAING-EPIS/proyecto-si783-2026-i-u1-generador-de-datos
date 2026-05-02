using DataGenerator.API.Models;
using DataGenerator.API.Adapters;
using System.Text;
using System.Text.Json;

namespace DataGenerator.API.Exporters;

public class ElasticsearchExporter : IDynamicExporter
{
    public string Export(List<Dictionary<string, object>> data, DynamicTableRequest request)
    {
        var adapter = new ElasticsearchAdapter();
        var sb = new StringBuilder();

        // 1. Mapping del índice
        sb.AppendLine("# === INDEX MAPPING ===");
        sb.AppendLine(adapter.GetCreateTableScript(request.TableName, request.Columns));
        sb.AppendLine();
        sb.AppendLine("# === DOCUMENTS ===");
        sb.AppendLine();

        // 2. Un POST por documento — sin duplicar la línea
        foreach (var row in data)
        {
            var doc = new Dictionary<string, object?>();
            foreach (var col in request.Columns)
                doc[col.Name] = row[col.Name];

            string docJson = JsonSerializer.Serialize(doc, new JsonSerializerOptions
            {
                WriteIndented = true
            });

            sb.AppendLine($"POST /{request.TableName}/_doc");
            sb.AppendLine(docJson);
            sb.AppendLine();
        }

        return sb.ToString();
    }

    public string GetFileExtension() => ".es.json";
}