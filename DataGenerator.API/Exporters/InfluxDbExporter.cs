using DataGenerator.API.Models;
using System.Text;

namespace DataGenerator.API.Exporters;

// InfluxDB usa "Line Protocol" como formato de escritura nativo
public class InfluxDbExporter : IDynamicExporter
{
    public string Export(List<Dictionary<string, object>> data, DynamicTableRequest request)
    {
        var sb = new StringBuilder();

        sb.AppendLine($"# InfluxDB Line Protocol — measurement: {request.TableName}");
        sb.AppendLine($"# Formato: measurement,tags fields timestamp");
        sb.AppendLine();

        long baseTimestamp = DateTimeOffset.UtcNow.Ticks * 100;
        for (int i = 0; i < data.Count; i++)
        {
            var row = data[i];
            var fields = new List<string>();

            foreach (var col in request.Columns)
            {
                var value = row[col.Name];
                string formatted = FormatInfluxValue(value, col);
                if (formatted != null)
                    fields.Add($"{col.Name}={formatted}");
            }

            if (!fields.Any()) continue;

            // timestamp incremental en nanosegundos
            long timestamp = baseTimestamp + (i * 1_000_000_000L);

            sb.AppendLine($"{request.TableName} {string.Join(",", fields)} {timestamp}");
        }

        return sb.ToString();
    }

    private string? FormatInfluxValue(object value, ColumnDefinition col)
    {
        if (value == null) return null;

        return col.Type switch
        {
            DataType.Integer                              => $"{value}i",
            DataType.Decimal or DataType.Amount
                or DataType.Price or DataType.Latitude
                or DataType.Longitude                    => value.ToString()!.Replace(",", "."),
            DataType.Boolean                              => (bool)value ? "true" : "false",
            DataType.DateTime                             => null, // se usa como timestamp
            _                                             => $"\"{value.ToString()?.Replace("\"", "\\\"")}\"",
        };
    }

    public string GetFileExtension() => ".lp";
}