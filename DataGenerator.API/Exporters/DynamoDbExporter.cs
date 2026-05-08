using DataGenerator.API.Models;
using System.Text;
using System.Text.Json;

namespace DataGenerator.API.Exporters;

// Genera comandos AWS CLI para PutItem en DynamoDB
public class DynamoDbExporter : IDynamicExporter
{
    public string Export(List<Dictionary<string, object>> data, DynamicTableRequest request)
    {
        var sb = new StringBuilder();

        sb.AppendLine($"# DynamoDB — AWS CLI PutItem commands");
        sb.AppendLine($"# Table: {request.TableName}");
        sb.AppendLine($"# Records: {data.Count}");
        sb.AppendLine();

        foreach (var row in data)
        {
            var item = new Dictionary<string, object>();

            foreach (var col in request.Columns)
            {
                var value = row[col.Name];
                item[col.Name] = BuildDynamoAttribute(value, col);
            }

            string itemJson = JsonSerializer.Serialize(item, new JsonSerializerOptions
            {
                WriteIndented = true
            });

            sb.AppendLine($"aws dynamodb put-item \\");
            sb.AppendLine($"  --table-name {request.TableName} \\");
            sb.AppendLine($"  --item '{itemJson}'");
            sb.AppendLine();
        }

        return sb.ToString();
    }

    private object BuildDynamoAttribute(object value, ColumnDefinition col)
    {
        if (value == null)
            return new { NULL = true };

        return col.Type switch
        {
            DataType.Integer                              => new { N = value.ToString() },
            DataType.Decimal or DataType.Amount
                or DataType.Price                        => new { N = value.ToString() },
            DataType.Boolean                              => new { BOOL = (bool)value },
            _                                             => new { S = value.ToString() }
        };
    }

    public string GetFileExtension() => ".dynamo.json";
}