using DataGenerator.API.Models;

namespace DataGenerator.API.Adapters;

public class Neo4jAdapter : IDatabaseAdapter
{
    public string Name => "Neo4j";

    public string GetCreateTableScript(string label, List<ColumnDefinition> columns)
    {
        // Neo4j no tiene DDL como SQL. Creamos un índice sobre el primer campo
        var firstCol = columns.FirstOrDefault();
        if (firstCol == null) return $"// No columns defined for label {label}";
        return $"CREATE INDEX {label.ToLower()}_idx IF NOT EXISTS FOR (n:{label}) ON (n.{firstCol.Name});";
    }

    public string GetColumnType(ColumnDefinition column) => "property";

    public string FormatValue(object value, ColumnDefinition column)
    {
        if (value == null) return "null";
        if (value is bool b) return b ? "true" : "false";
        if (value is DateTime dt) return $"datetime('{dt:yyyy-MM-ddTHH:mm:ss}Z')";
        if (value is int || value is long || value is decimal || value is double)
            return value.ToString()!;
        return $"'{value.ToString()?.Replace("'", "\\'")}'";
    }

    public string GetInsertScript(string label, List<ColumnDefinition> columns, Dictionary<string, object> row)
    {
        var props = columns.Select(c => $"{c.Name}: {FormatValue(row[c.Name], c)}");
        return $"CREATE (:{label} {{{string.Join(", ", props)}}});";
    }

    public string GetConnectionStringExample()
        => "bolt://localhost:7687";
}