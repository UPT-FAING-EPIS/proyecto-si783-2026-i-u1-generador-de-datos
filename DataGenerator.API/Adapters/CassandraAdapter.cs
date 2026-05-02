using DataGenerator.API.Models;

namespace DataGenerator.API.Adapters;

public class CassandraAdapter : IDatabaseAdapter
{
    public string Name => "Cassandra";

    public string GetCreateTableScript(string tableName, List<ColumnDefinition> columns)
    {
        var columnsDef = columns.Select(col =>
            $"    {col.Name} {GetColumnType(col)}");

        // Primera columna como partition key por convención
        var firstCol = columns.FirstOrDefault()?.Name ?? "id";

        return $@"CREATE TABLE IF NOT EXISTS {tableName} (
{string.Join(",\n", columnsDef)},
    PRIMARY KEY ({firstCol})
);";
    }

    public string GetColumnType(ColumnDefinition column)
    {
        return column.Type switch
        {
            DataType.Integer                          => "int",
            DataType.Decimal or DataType.Amount
                or DataType.Price                     => "decimal",
            DataType.Boolean                          => "boolean",
            DataType.DateTime                         => "timestamp",
            DataType.Date                             => "date",
            DataType.Guid or DataType.UUID            => "uuid",
            DataType.Text or DataType.Paragraph
                or DataType.Sentence                  => "text",
            _                                         => "text"
        };
    }

    public string FormatValue(object value, ColumnDefinition column)
    {
        if (value == null) return "null";
        if (value is bool b) return b ? "true" : "false";
        if (value is int || value is decimal || value is double)
            return value.ToString()!;
        if (value is DateTime dt) return $"'{dt:yyyy-MM-dd HH:mm:ss}'";
        return $"'{value.ToString()?.Replace("'", "''")}'";
    }

    public string GetInsertScript(string tableName, List<ColumnDefinition> columns, Dictionary<string, object> row)
    {
        var names = columns.Select(c => c.Name);
        var values = columns.Select(c => FormatValue(row[c.Name], c));
        return $"INSERT INTO {tableName} ({string.Join(", ", names)}) VALUES ({string.Join(", ", values)});";
    }

    public string GetConnectionStringExample()
        => "Contact Points=localhost;Port=9042;";
}