using DataGenerator.API.Models;
using System.Text;
using System.Text.Json;

namespace DataGenerator.API.Adapters;

public class ElasticsearchAdapter : IDatabaseAdapter
{
    public string Name => "Elasticsearch";

    public string GetCreateTableScript(string indexName, List<ColumnDefinition> columns)
    {
        // En Elasticsearch se crea un "mapping" en lugar de una tabla
        var properties = new Dictionary<string, object>();

        foreach (var col in columns)
        {
            properties[col.Name] = new { type = GetEsType(col) };
        }

        var mapping = new
        {
            mappings = new { properties }
        };

        return $"PUT /{indexName}\n" +
               JsonSerializer.Serialize(mapping, new JsonSerializerOptions { WriteIndented = true });
    }

    public string GetColumnType(ColumnDefinition column) => GetEsType(column);

    public string FormatValue(object value, ColumnDefinition column)
    {
        if (value == null) return "null";
        if (value is bool b) return b ? "true" : "false";
        if (value is DateTime dt) return $"\"{dt:yyyy-MM-ddTHH:mm:ssZ}\"";
        if (value is int || value is long || value is decimal || value is double)
            return value.ToString()!;
        return $"\"{value.ToString()?.Replace("\"", "\\\"")}\"";
    }

    public string GetInsertScript(string indexName, List<ColumnDefinition> columns, Dictionary<string, object> row)
    {
    // Solo devuelve el JSON del documento, sin el POST
    // (el exporter se encarga de escribir la línea POST)
    var doc = new Dictionary<string, object?>();
    foreach (var col in columns)
        doc[col.Name] = row[col.Name];

    return JsonSerializer.Serialize(doc, new JsonSerializerOptions { WriteIndented = true });
}

    public string GetConnectionStringExample()
        => "http://localhost:9200";

    private string GetEsType(ColumnDefinition col)
    {
        return col.Type switch
        {
            DataType.Integer                          => "integer",
            DataType.Decimal or DataType.Amount
                or DataType.Price                     => "float",
            DataType.Boolean                          => "boolean",
            DataType.DateTime                         => "date",
            DataType.Date                             => "date",
            DataType.Latitude or DataType.Longitude   => "float",
            DataType.Text or DataType.Paragraph
                or DataType.Sentence                  => "text",
            _                                         => "keyword"
        };
    }
}